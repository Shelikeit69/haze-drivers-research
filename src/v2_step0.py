"""Plan v2, Step 0: build fire events from FIRMS and validate against Sloan et al. (Dryad).

Plan: docs/research_plan_v2.md (frozen 2 Nov 2026). Definitions used here:
  - detections are MODIS_SP (Collection 6.1), data/raw/firms plus data/raw/firms_v2,
    1 Jun 2002 - 31 Jan 2020 (the 2002-2019 validation window plus edge detections);
  - 1 km equal-area grid: MODIS sinusoidal projection, 1 km cells;
  - 8-neighbour (or 4-neighbour) adjacency, detections within 4 days;
  - ignition date = earliest detection date; event kept when ignition is Jul-Dec 2002-2019;
  - severity = sum(FRP) * (duration in days + 1), as FRP_Days in Sloan's tables;
  - severe >= 60.4, very severe >= 216 (Sloan's national thresholds).

Dryad side: detections are restricted to the v1 island boxes by POINT_X/POINT_Y. An event
is kept when at least one of its detections falls in a box, assigned to the box holding
most of its detections, and kept when its ignition (MIN_acq_yer, MIN_acq_mnt) is
Jul-Dec 2002-2019. The Dryad Island code is used only as a cross-check.

Pass rule: both islands, yearly severe-event Pearson r >= 0.95, and the 18-season
totals of events and severe events each within +/-10% of Dryad. If the primary
(8-neighbour, all detections) fails, the plan's fallbacks are run in order:
4-neighbour, then type-0 detections only (both applied to the 4-neighbour variant).

Usage: python src/v2_step0.py
"""
import glob
import hashlib
import os
import sys
from bisect import bisect_left, bisect_right

import numpy as np
import pandas as pd
from scipy import stats

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
RES = sys.argv[2] if len(sys.argv) > 2 else "results"
DRYAD = os.path.join("data", "external", "sloan_dryad", "Dryad_Version_ofGDB")
ISLANDS = ["sumatra", "kalimantan"]
YEARS = list(range(2002, 2020))
SEVERE = 60.4
VERY_SEVERE = 216.0
START = pd.Timestamp("2002-06-01")
END = pd.Timestamp("2020-01-31")
R_EARTH_KM = 6371.0072
DRYAD_ZIP = os.path.join("data", "external", "sloan_dryad",
                         "doi_10_5061_dryad_msbcc2g1t__v20220828.zip")
DRYAD_SHA256 = "0b76226376a13cc8212df0f07041597cd169fba9c7cbdcd8cb6541e80a789e3b"


def island(lat, lon):
    """v1 island boxes, copied from src/analyse_r4.py so they stay identical."""
    if 100 <= lon <= 106.5 and -5 <= lat <= 1.0:
        return "sumatra"
    if 100 <= lon <= 101.9 and 1.0 < lat <= 2.3:
        return "sumatra"
    if 108.5 <= lon <= 116.5 and -4.5 <= lat <= 1.0:
        return "kalimantan"
    return "other"


ISLAND_VEC = np.vectorize(island, otypes=[object])


# ---------- FIRMS detections ----------
def load_firms():
    frames = []
    for folder in (os.path.join(RAW, "firms"), os.path.join(RAW, "firms_v2")):
        for p in sorted(glob.glob(os.path.join(folder, "MODIS_SP_*.csv"))):
            d = pd.read_csv(p)
            if d.empty:
                continue
            frames.append(d)
    f = pd.concat(frames, ignore_index=True)
    keep = ["latitude", "longitude", "acq_date", "frp", "type", "satellite"]
    f = f[keep].drop_duplicates().reset_index(drop=True)
    f["acq_date"] = pd.to_datetime(f["acq_date"])
    f = f[(f["acq_date"] >= START) & (f["acq_date"] <= END)].reset_index(drop=True)
    f["island"] = ISLAND_VEC(f["latitude"].to_numpy(), f["longitude"].to_numpy())
    return f


def grid_cells(lat, lon):
    """1 km equal-area cells in the MODIS sinusoidal projection."""
    latr = np.radians(lat)
    x = R_EARTH_KM * np.radians(lon) * np.cos(latr)
    y = R_EARTH_KM * latr
    return np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)


def neighbours(adjacency):
    if adjacency == 8:
        return [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    return [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def build_events(firms, adjacency, type0_only=False):
    """Connected components of detections linked in space (cell adjacency) and time (4 days)."""
    d = firms[firms["island"] != "other"].copy()
    if type0_only:
        d = d[d["type"] == 0].copy()
    d = d.reset_index(drop=True)
    n = len(d)
    parent = np.arange(n, dtype=np.int64)
    size = np.ones(n, dtype=np.int64)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    cx, cy = grid_cells(d["latitude"].to_numpy(), d["longitude"].to_numpy())
    date_ord = (d["acq_date"] - START).dt.days.to_numpy()
    offsets = neighbours(adjacency)

    for isl in ISLANDS:
        sel = np.where(d["island"].to_numpy() == isl)[0]
        cells = {}
        for i in sel:
            key = (int(cx[i]), int(cy[i]))
            cells.setdefault(key, []).append(i)
        # sort each cell's detections by date, keep parallel date arrays
        packed = {k: (np.array(sorted(v, key=lambda j: date_ord[j]), dtype=np.int64))
                  for k, v in cells.items()}
        for k, idx in packed.items():
            dates = date_ord[idx]
            for dx, dy in offsets:
                nb = packed.get((k[0] + dx, k[1] + dy))
                if nb is None:
                    continue
                nb_dates = date_ord[nb]
                for pos, i in enumerate(idx):
                    lo = bisect_left(nb_dates, dates[pos] - 4)
                    hi = bisect_right(nb_dates, dates[pos] + 4)
                    for j in nb[lo:hi]:
                        if i != j:
                            union(int(i), int(j))

    root = np.array([find(i) for i in range(n)], dtype=np.int64)
    d["event"] = root
    ev = d.groupby("event").agg(
        ignition=("acq_date", "min"),
        last=("acq_date", "max"),
        frp_sum=("frp", "sum"),
        island=("island", "first"),
        n_det=("acq_date", "size"),
    )
    ev["duration"] = (ev["last"] - ev["ignition"]).dt.days
    ev["severity"] = ev["frp_sum"] * (ev["duration"] + 1)
    ev["year"] = ev["ignition"].dt.year
    ev["month"] = ev["ignition"].dt.month
    ev = ev[(ev["year"].isin(YEARS)) & (ev["month"].between(7, 12))]
    return ev.reset_index(drop=True), len(d)


def summarise(events, source, scenario):
    """Yearly event counts by island and year."""
    rows = []
    for isl in ISLANDS:
        for y in YEARS:
            g = events[(events["island"] == isl) & (events["year"] == y)]
            rows.append({
                "scenario": scenario, "source": source, "island": isl, "year": y,
                "n_events": len(g),
                "n_severe": int((g["severity"] >= SEVERE).sum()),
                "n_very_severe": int((g["severity"] >= VERY_SEVERE).sum()),
                "median_severity": float(g["severity"].median()) if len(g) else np.nan,
            })
    return pd.DataFrame(rows)


# ---------- Dryad side ----------
DRYAD_COLS = ["MIN_acq_yer", "MIN_acq_mnt", "AF_Count", "nfireID2", "Island",
              "FRP_Days", "POINT_X", "POINT_Y"]


def load_dryad():
    p = os.path.join(DRYAD, "nfire4_all_spatial_fire_2002_2019_joins_sp_LC.csv")
    d = pd.read_csv(p, usecols=DRYAD_COLS, low_memory=False)
    d["our_island"] = ISLAND_VEC(d["POINT_Y"].to_numpy(), d["POINT_X"].to_numpy())

    # cross-check: Dryad Island code against the coordinate-based box
    code_map = {1000000: "sumatra", 2000000: "kalimantan"}
    code_island = d["Island"].map(code_map).fillna("other")
    in_box = d["our_island"] != "other"
    x = d[in_box]
    code_x = code_island[in_box]
    both = (code_x != "other") & (code_x != x["our_island"])
    cross = {
        "detections_in_boxes": int(in_box.sum()),
        "detections_other_or_missing_code": int((code_x == "other").sum()),
        "detections_code_vs_coords_mismatch": int(both.sum()),
    }

    sub = d[in_box]
    # assign an event to the box holding most of its detections
    cnt = sub.groupby(["nfireID2", "our_island"]).size().reset_index(name="n")
    cnt = cnt.sort_values(["nfireID2", "n"], ascending=[True, False])
    ev_island = cnt.drop_duplicates("nfireID2").set_index("nfireID2")["our_island"]

    ev = sub.drop_duplicates("nfireID2").set_index("nfireID2")
    ev["our_island"] = ev_island.reindex(ev.index)
    ev["code_island"] = ev["Island"].map(code_map).fillna("other")
    ev["year"] = ev["MIN_acq_yer"].astype(int)
    ev["month"] = ev["MIN_acq_mnt"].astype(int)
    ev = ev[(ev["year"].isin(YEARS)) & (ev["month"].between(7, 12))]
    ev["island"] = ev["our_island"]
    ev["severity"] = ev["FRP_Days"]

    # cross-check on kept events
    kept = ev.copy()
    cross.update({
        "events_in_boxes": int(len(sub.drop_duplicates("nfireID2"))),
        "events_kept_jul_dec_2002_2019": int(len(kept)),
        "events_code_missing_or_other": int((kept["code_island"] == "other").sum()),
        "events_code_vs_coords_mismatch": int(((kept["code_island"] != "other") &
                                               (kept["code_island"] != kept["island"])).sum()),
    })
    return kept, cross


def compare(scenario, ours, dryad, ours_events, dryad_events):
    rows = []
    for isl in ISLANDS:
        o = ours[(ours["scenario"] == scenario) & (ours["island"] == isl)].sort_values("year")
        d = dryad[dryad["island"] == isl].sort_values("year")
        assert list(o["year"]) == YEARS and list(d["year"]) == YEARS
        co = o.set_index("year")
        cd = d.set_index("year")
        med_diff = (co["median_severity"] - cd["median_severity"]).abs().max()
        r_ev = stats.pearsonr(co["n_events"], cd["n_events"])[0]
        r_sv = stats.pearsonr(co["n_severe"], cd["n_severe"])[0]
        r_vs = stats.pearsonr(co["n_very_severe"], cd["n_very_severe"])[0]
        ev_o, ev_d = int(co["n_events"].sum()), int(cd["n_events"].sum())
        sv_o, sv_d = int(co["n_severe"].sum()), int(cd["n_severe"].sum())
        pass_ev = abs(ev_o / ev_d - 1) <= 0.10 if ev_d else False
        pass_sv = abs(sv_o / sv_d - 1) <= 0.10 if sv_d else False
        pass_r = bool(np.isfinite(r_sv) and r_sv >= 0.95)
        rows.append({
            "scenario": scenario, "island": isl, "years": "2002-2019",
            "r_events": r_ev, "r_severe": r_sv, "r_very_severe": r_vs,
            "events_ours": ev_o, "events_dryad": ev_d, "events_ratio": ev_o / ev_d,
            "severe_ours": sv_o, "severe_dryad": sv_d, "severe_ratio": sv_o / sv_d,
            "median_severity_ours": float(ours_events.loc[
                (ours_events["scenario"] == scenario) & (ours_events["island"] == isl),
                "severity"].median()),
            "median_severity_dryad": float(dryad_events.loc[
                dryad_events["island"] == isl, "severity"].median()),
            "max_abs_yearly_median_diff": float(med_diff),
            "pass_r": pass_r, "pass_events_totals": bool(pass_ev),
            "pass_severe_totals": bool(pass_sv),
            "pass_island": bool(pass_r and pass_ev and pass_sv),
        })
    out = pd.DataFrame(rows)
    out["pass_scenario"] = bool(out["pass_island"].all())
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def empty_v2_files():
    rows = []
    for p in sorted(glob.glob(os.path.join(RAW, "firms_v2", "MODIS_SP_*.csv"))):
        with open(p) as fh:
            n = sum(1 for _ in fh) - 1
        if n <= 0:
            rows.append({"file": os.path.basename(p), "data_rows": 0})
    return pd.DataFrame(rows)


def main():
    os.makedirs(RES, exist_ok=True)
    firms = load_firms()
    print(f"FIRMS detections in window: {len(firms)}; other (dropped): "
          f"{int((firms['island'] == 'other').sum())}")

    dryad_events, cross = load_dryad()
    dryad_yearly = summarise(dryad_events, "dryad", "dryad")

    yearly, comparisons = [], []
    attempts = [("8-neighbour, all detections", 8, False),
                ("4-neighbour, all detections", 4, False),
                ("4-neighbour, type-0 detections", 4, True)]
    passed = False
    for label, adj, t0 in attempts:
        ev, n_used = build_events(firms, adj, type0_only=t0)
        print(f"{label}: {n_used} detections -> {len(ev)} events")
        ours = summarise(ev, "ours", label)
        yearly.append(ours)
        comp = compare(label, ours, dryad_yearly, ev.assign(scenario=label), dryad_events)
        comp.insert(1, "detections_used", n_used)
        comparisons.append(comp)
        if comp["pass_scenario"].all():
            passed = True
            break

    y = pd.concat([dryad_yearly] + yearly, ignore_index=True)
    y.to_csv(os.path.join(RES, "v2_step0_yearly.csv"), index=False)
    c = pd.concat(comparisons, ignore_index=True)
    c.to_csv(os.path.join(RES, "v2_step0_comparison.csv"), index=False)
    actual = sha256(DRYAD_ZIP) if os.path.exists(DRYAD_ZIP) else "not_downloaded"
    cross["firms_detections_window"] = int(len(firms))
    cross["firms_detections_other_dropped"] = int((firms["island"] == "other").sum())
    cross["dryad_zip_sha256"] = actual
    cross["dryad_zip_sha256_matches_plan"] = bool(actual == DRYAD_SHA256)
    x = pd.DataFrame([cross])
    x.to_csv(os.path.join(RES, "v2_step0_crosscheck.csv"), index=False)
    empty_v2_files().to_csv(os.path.join(RES, "v2_step0_empty_firms_v2.csv"), index=False)

    pd.set_option("display.width", 240)
    pd.set_option("display.max_columns", 40)
    print()
    print(c[["scenario", "island", "r_events", "r_severe", "r_very_severe",
             "events_ours", "events_dryad", "events_ratio", "severe_ours", "severe_dryad",
             "severe_ratio", "pass_island"]].round(4).to_string(index=False))
    print()
    print(x.T.to_string())
    print()
    print("primary passed:", bool(comparisons[0]["pass_scenario"].all()))
    print("scenario selected:", attempts[len(comparisons) - 1][0] if passed else "none")


if __name__ == "__main__":
    main()
