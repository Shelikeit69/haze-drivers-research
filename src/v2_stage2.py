"""Plan v2, Stage 2: Step 1 replication, T1-T2, Holm, robustness, exploratory.

Plan: docs/research_plan_v2.md (frozen 2 Nov 2026) plus the 2 Nov 2026 Deviations.

All fire events are built by src/v2_step0.build_events (8-neighbour, all detections),
the validated configuration. 2002-2025 uses the same function with an extended year range.

Rain: GPCP v2.3, three v1 cells per island (results/gpcp_cells_r3.csv), Jul-Dec total in mm
(monthly mm/day x days in month, summed), same algorithm as src/v2_q3.rain.

Outputs:
  results/v2_step1_models.csv       Step 1 (a) severe/very-severe and (b) skewness, 2002-2019
  results/v2_step1_yearly.csv       yearly inputs for Step 1
  results/v2_t1t2_primary.csv       T1/T2 2002-2025 WLS, p-values, bootstrap, LOO
  results/v2_t1t2_robustness.csv    T1/T2 robustness (post2016 step, block bootstrap, LOO, Aqua)
  results/v2_t1t2_yearly.csv        yearly inputs for T1/T2
  results/v2_holm.csv               Holm correction over T1-T6
  results/v2_exploratory_skewness.csv, results/v2_exploratory_2019_vs_2023.csv
  results/v2_viirs_chirps_status.csv
  results/v2_event_build_summary.csv  detections used and events kept (2002-2025)
  results/v2_t1t2_trend.png, results/v2_exploratory_frp_rain.png

Usage: python src/v2_stage2.py
"""
import os
import sys

import netCDF4 as nc
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import src.v2_step0 as v2_step0  # noqa: E402

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
RES = sys.argv[2] if len(sys.argv) > 2 else "results"

ISLANDS = ["sumatra", "kalimantan"]
SEVERE = 60.4
VERY_SEVERE = 216.0
SEED = 20261102
STEP1_B = 1000
T1T2_B = 10000
GROUP = {"sumatra": ["riau", "jambi", "south_sumatra"],
         "kalimantan": ["west_kalimantan", "central_kalimantan", "south_kalimantan"]}

# Sloan et al. 2022 published ranges (for side-by-side reporting only)
SLOAN = {
    "severe_pct": (19.0, 27.0),
    "very_severe_pct": (23.0, 34.0),
    "sumatra_severity_pct": (-16.0,),  # single reported value, Sumatra seasonal severity -16%
}


# ---------- rain (GPCP, same algorithm as v2_q3.rain) ----------
def load_rain():
    cells = pd.read_csv(os.path.join(RES, "gpcp_cells_r3.csv")).set_index("point")
    ds = nc.Dataset(os.path.join(RAW, "noaa_psl_gpcp_v2.3_precip.mon.mean.nc"))
    lat = np.array(ds.variables["lat"][:])
    lon = np.array(ds.variables["lon"][:])
    t = ds.variables["time"]
    dates = pd.to_datetime([f"{d.year}-{d.month:02d}-01" for d in nc.num2date(t[:], t.units)])
    pr = np.ma.filled(ds.variables["precip"][:].astype(float), np.nan)
    ser = {}
    for p, r in cells.iterrows():
        i = int(np.where(np.isclose(lat, r["cell_lat"]))[0][0])
        j = int(np.where(np.isclose(lon, r["cell_lon"]))[0][0])
        ser[p] = pd.Series(pr[:, i, j], index=dates)
    g = pd.DataFrame(ser)
    days = g.index.days_in_month

    def rain(isl, y, months):
        s = g.loc[(g.index.year == y) & g.index.month.isin(months), GROUP[isl]]
        if len(s) != len(months) or s.isna().any().any():
            return np.nan
        m = s.mean(axis=1)
        return float((m * days[(g.index.year == y) & g.index.month.isin(months)]).sum())

    rows = []
    for y in range(2002, 2026):
        for isl in ISLANDS:
            rows.append({"year": y, "island": isl,
                         "rain_juldec": rain(isl, y, [7, 8, 9, 10, 11, 12])})
    return pd.DataFrame(rows)


# ---------- events ----------
def build_all_events(aqua_only=False):
    start = pd.Timestamp("2002-06-01")
    end = pd.Timestamp("2026-01-31")
    firms = v2_step0.load_firms(start=start, end=end)
    if aqua_only:
        firms = firms[firms["satellite"] == "Aqua"].copy()
    years = list(range(2002, 2026))
    ev, n_used = v2_step0.build_events(firms, 8, type0_only=False, years=years, start=start)
    return ev, n_used


def yearly_table(events, rain):
    rows = []
    for isl in ISLANDS:
        for y in range(2002, 2026):
            g = events[(events["island"] == isl) & (events["year"] == y)]
            sev = g["severity"].to_numpy(float)
            rows.append({
                "island": isl, "year": y,
                "n_events": len(g),
                "n_severe": int((sev >= SEVERE).sum()),
                "n_very_severe": int((sev >= VERY_SEVERE).sum()),
                "fire_points": int(g["n_det"].sum()),
                "prop_severe": (sev >= SEVERE).mean() if len(g) else np.nan,
                "prop_very_severe": (sev >= VERY_SEVERE).mean() if len(g) else np.nan,
                "skewness": float(stats.skew(sev, bias=False)) if len(g) > 2 else np.nan,
                "frp_sum": float(g["frp_sum"].sum()),
            })
    df = pd.DataFrame(rows)
    df = df.merge(rain, on=["island", "year"])
    df["year0"] = df["year"] - 2002
    return df


# ---------- fitting helpers ----------
def fit_wls(df, y_col, x_cols, weight_col):
    sub = df[[y_col] + x_cols + [weight_col]].dropna()
    X = sm.add_constant(sub[x_cols])
    m = sm.WLS(sub[y_col], X, weights=sub[weight_col]).fit()
    return m, sub


def fit_ols(df, y_col, x_cols):
    sub = df[[y_col] + x_cols].dropna()
    X = sm.add_constant(sub[x_cols])
    m = sm.OLS(sub[y_col], X).fit()
    return m, sub


def pct_change_17yr(m, mean_rain, rain_col, year_col):
    """100 * 17 * b / fitted value in year 2002 at sample-mean rain."""
    b = float(m.params[year_col])
    const = float(m.params["const"])
    rc = float(m.params[rain_col]) if rain_col in m.params else 0.0
    base = const + rc * mean_rain
    return 100.0 * 17.0 * b / base if base != 0 else np.nan


def bootstrap_pct(df, y_col, x_cols, weight_col, rain_col, year_col, mean_rain,
                  n_boot, rng, wls=True):
    """Resample years, refit, return array of % change over 17 years."""
    sub = df[[y_col] + x_cols + ([weight_col] if wls else [])].dropna().reset_index(drop=True)
    n = len(sub)
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        s = sub.iloc[idx]
        X = np.column_stack([np.ones(n), s[x_cols].to_numpy(float)])
        y = s[y_col].to_numpy(float)
        if wls:
            w = s[weight_col].to_numpy(float)
            if w.sum() <= 0:
                continue
            beta = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
        else:
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
        # parameter order: const, then x_cols in order
        b = beta[1 + x_cols.index(year_col)]
        const = beta[0]
        rc = beta[1 + x_cols.index(rain_col)] if rain_col in x_cols else 0.0
        base = const + rc * mean_rain
        if base != 0:
            vals.append(100.0 * 17.0 * b / base)
    return np.array(vals)


# ---------- Step 1 ----------
def run_step1(yearly):
    rows = []
    rng = np.random.default_rng(SEED)
    for isl in ISLANDS:
        d = yearly[(yearly["island"] == isl) & (yearly["year"].between(2002, 2019))].copy()
        mean_rain = float(d["rain_juldec"].mean())
        for outcome, ycol, wls in [
            ("severe", "prop_severe", True),
            ("very_severe", "prop_very_severe", True),
            ("skewness", "skewness", False),
        ]:
            x_cols = ["rain_juldec", "year0"]
            if wls:
                m, _ = fit_wls(d, ycol, x_cols, "fire_points")
                pct = pct_change_17yr(m, mean_rain, "rain_juldec", "year0")
                boot = bootstrap_pct(d, ycol, x_cols, "fire_points", "rain_juldec", "year0",
                                     mean_rain, STEP1_B, rng, wls=True)
            else:
                m, _ = fit_ols(d, ycol, x_cols)
                pct = pct_change_17yr(m, mean_rain, "rain_juldec", "year0")
                boot = bootstrap_pct(d, ycol, x_cols, None, "rain_juldec", "year0",
                                     mean_rain, STEP1_B, rng, wls=False)
            lo, hi = np.percentile(boot, [2.5, 97.5]) if len(boot) else (np.nan, np.nan)
            rows.append({
                "island": isl, "outcome": outcome, "years": "2002-2019", "n": len(d),
                "method": "WLS" if wls else "OLS",
                "year_coef": float(m.params["year0"]),
                "rain_coef": float(m.params["rain_juldec"]),
                "pct_change_17yr": pct,
                "boot95_low": float(lo), "boot95_high": float(hi),
                "sloan_range": _sloan_ref(outcome, isl),
            })
        # drop-2015 and drop-2019 for severe only (Sloan's robustness)
        for drop in (2015, 2019):
            d2 = d[d["year"] != drop].copy()
            mr = float(d2["rain_juldec"].mean())
            m, _ = fit_wls(d2, "prop_severe", ["rain_juldec", "year0"], "fire_points")
            pct = pct_change_17yr(m, mr, "rain_juldec", "year0")
            boot = bootstrap_pct(d2, "prop_severe", ["rain_juldec", "year0"], "fire_points",
                                 "rain_juldec", "year0", mr, STEP1_B, rng, wls=True)
            lo, hi = np.percentile(boot, [2.5, 97.5]) if len(boot) else (np.nan, np.nan)
            rows.append({
                "island": isl, "outcome": f"severe_drop{drop}", "years": f"2002-2019,-{drop}",
                "n": len(d2), "method": "WLS",
                "year_coef": float(m.params["year0"]),
                "rain_coef": float(m.params["rain_juldec"]),
                "pct_change_17yr": pct,
                "boot95_low": float(lo), "boot95_high": float(hi),
                "sloan_range": _sloan_ref("severe", isl),
            })
    return pd.DataFrame(rows)


def _sloan_ref(outcome, isl):
    if outcome.startswith("severe"):
        return f"{SLOAN['severe_pct'][0]}-{SLOAN['severe_pct'][1]}%"
    if outcome == "very_severe":
        return f"{SLOAN['very_severe_pct'][0]}-{SLOAN['very_severe_pct'][1]}%"
    if outcome == "skewness" and isl == "sumatra":
        return f"{SLOAN['sumatra_severity_pct'][0]}%"
    return ""


# ---------- T1 / T2 ----------
def run_t1t2(yearly):
    rows = []
    rng = np.random.default_rng(SEED + 10)
    for tid, isl in zip(["T1", "T2"], ISLANDS):
        d = yearly[yearly["island"] == isl].copy()
        mean_rain = float(d["rain_juldec"].mean())
        m, _ = fit_wls(d, "prop_severe", ["rain_juldec", "year0"], "fire_points")
        boot = bootstrap_pct(d, "prop_severe", ["rain_juldec", "year0"], "fire_points",
                             "rain_juldec", "year0", mean_rain, T1T2_B, rng, wls=True)
        lo, hi = np.percentile(boot, [2.5, 97.5]) if len(boot) else (np.nan, np.nan)
        # leave-one-year-out
        loo = []
        for y in d["year"]:
            s = d[d["year"] != y]
            mm, _ = fit_wls(s, "prop_severe", ["rain_juldec", "year0"], "fire_points")
            loo.append(float(mm.params["year0"]))
        rows.append({
            "id": tid, "island": isl, "years": "2002-2025", "n": len(d),
            "year_coef": float(m.params["year0"]),
            "se_year": float(m.bse["year0"]),
            "p_two_sided": float(m.pvalues["year0"]),
            "direction": "negative" if m.params["year0"] < 0 else "positive",
            "rain_coef": float(m.params["rain_juldec"]),
            "pct_change_17yr": pct_change_17yr(m, mean_rain, "rain_juldec", "year0"),
            "boot95_low": float(lo), "boot95_high": float(hi),
            "loo_year_coef_min": min(loo), "loo_year_coef_max": max(loo),
        })
    return pd.DataFrame(rows)


def run_t1t2_robustness(yearly, events_all):
    rows = []
    rng = np.random.default_rng(SEED + 20)
    for tid, isl in zip(["T1", "T2"], ISLANDS):
        d = yearly[yearly["island"] == isl].copy()
        mean_rain = float(d["rain_juldec"].mean())

        # rob2: post2016 step instead of linear year
        d2 = d.copy()
        d2["post2016"] = (d2["year"] >= 2016).astype(int)
        m, _ = fit_wls(d2, "prop_severe", ["rain_juldec", "post2016"], "fire_points")
        rows.append({"id": tid, "island": isl, "kind": "rob2 post2016 step",
                     "coef": float(m.params["post2016"]), "se": float(m.bse["post2016"]),
                     "p_two_sided": float(m.pvalues["post2016"])})

        # rob3: 3-year moving block bootstrap for the year coefficient
        sub = d[["prop_severe", "rain_juldec", "year0", "fire_points"]].dropna().reset_index(drop=True)
        n = len(sub)
        block = 3
        coefs = []
        for _ in range(T1T2_B):
            starts = rng.integers(0, n - block + 1, int(np.ceil(n / block)))
            idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
            s = sub.iloc[idx]
            X = np.column_stack([np.ones(n), s[["rain_juldec", "year0"]].to_numpy(float)])
            y = s["prop_severe"].to_numpy(float)
            w = s["fire_points"].to_numpy(float)
            beta = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
            coefs.append(beta[2])
        lo, hi = np.percentile(coefs, [2.5, 97.5])
        rows.append({"id": tid, "island": isl, "kind": "rob3 block bootstrap",
                     "coef": np.nan, "se": np.nan, "p_two_sided": np.nan,
                     "boot95_low": float(lo), "boot95_high": float(hi)})

        # rob4: leave-one-year-out range of year coef
        loo = []
        for y in d["year"]:
            s = d[d["year"] != y]
            mm, _ = fit_wls(s, "prop_severe", ["rain_juldec", "year0"], "fire_points")
            loo.append(float(mm.params["year0"]))
        rows.append({"id": tid, "island": isl, "kind": "rob4 leave-one-year-out",
                     "coef": np.nan, "se": np.nan, "p_two_sided": np.nan,
                     "loo_year_coef_min": min(loo), "loo_year_coef_max": max(loo)})

        # rob5: Aqua-only events
    # Aqua-only events built once outside the loop
    ev_aqua, _ = build_all_events(aqua_only=True)
    rain = load_rain()
    ytab_aqua = yearly_table(ev_aqua, rain)
    for tid, isl in zip(["T1", "T2"], ISLANDS):
        d = ytab_aqua[ytab_aqua["island"] == isl].copy()
        m, _ = fit_wls(d, "prop_severe", ["rain_juldec", "year0"], "fire_points")
        rows.append({"id": tid, "island": isl, "kind": "rob5 Aqua only",
                     "coef": float(m.params["year0"]), "se": float(m.bse["year0"]),
                     "p_two_sided": float(m.pvalues["year0"]),
                     "n_aqua_events": int(d["n_events"].sum())})
    return pd.DataFrame(rows)


# ---------- Holm ----------
def holm():
    q3 = pd.read_csv(os.path.join(RES, "v2_q3_results.csv"))
    q3p = q3[q3["kind"] == "primary"][["id", "p_raw"]].copy()
    q3p.columns = ["id", "p_raw"]
    t1t2 = pd.read_csv(os.path.join(RES, "v2_t1t2_primary.csv"))[["id", "p_two_sided"]]
    t1t2.columns = ["id", "p_raw"]
    p = pd.concat([t1t2, q3p], ignore_index=True)
    p = p.sort_values("p_raw").reset_index(drop=True)
    m = len(p)
    p["rank"] = np.arange(1, m + 1)
    p["holm_p"] = np.minimum(1.0, (m - p["rank"] + 1) * p["p_raw"])
    # enforce monotonicity (holm p is non-decreasing in rank)
    p["holm_p"] = p["holm_p"][::-1].cummin()[::-1]
    p["significant_0.05"] = p["holm_p"] < 0.05
    return p


# ---------- VIIRS (robustness 6) and CHIRPS (robustness 8) ----------
def viirs():
    key = os.environ.get("FIRMS_MAP_KEY")
    if not key:
        return pd.DataFrame([{"test": "VIIRS", "status": "not run",
                              "reason": "FIRMS_MAP_KEY not set in the environment"}])
    # Not implemented here; would download VIIRS_SNPP_SP Aug-Oct 2012-2025.
    return pd.DataFrame([{"test": "VIIRS", "status": "not run",
                          "reason": "FIRMS_MAP_KEY present but download not implemented in this run"}])


def chirps():
    return pd.DataFrame([{"test": "CHIRPS", "status": "not run",
                          "reason": "no working download"}])


# ---------- exploratory ----------
def exploratory(yearly, events):
    rows = []
    # skewness 2002-2025
    for isl in ISLANDS:
        for y in range(2002, 2026):
            g = events[(events["island"] == isl) & (events["year"] == y)]
            sev = g["severity"].to_numpy(float)
            rows.append({"island": isl, "year": y, "n_events": len(g),
                         "skewness": float(stats.skew(sev, bias=False)) if len(sev) > 2 else np.nan,
                         "median_severity": float(np.median(sev)) if len(sev) else np.nan,
                         "frp_sum": float(g["frp_sum"].sum()),
                         "rain_juldec": float(yearly[(yearly.island == isl) & (yearly.year == y)]["rain_juldec"].iloc[0])})
    sk = pd.DataFrame(rows)

    # 2019 vs 2023
    comp = []
    for isl in ISLANDS:
        for y in (2019, 2023):
            g = events[(events["island"] == isl) & (events["year"] == y)]
            sev = g["severity"].to_numpy(float)
            r = float(yearly[(yearly.island == isl) & (yearly.year == y)]["rain_juldec"].iloc[0])
            comp.append({"island": isl, "year": y, "n_events": len(g),
                         "n_severe": int((sev >= SEVERE).sum()),
                         "n_very_severe": int((sev >= VERY_SEVERE).sum()),
                         "median_severity": float(np.median(sev)) if len(sev) else np.nan,
                         "mean_severity": float(sev.mean()) if len(sev) else np.nan,
                         "frp_sum": float(g["frp_sum"].sum()),
                         "rain_juldec": r})
    cmp = pd.DataFrame(comp)
    return sk, cmp


def make_plots(yearly, events):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # T1/T2 trend plot: severe proportion vs year, by island, with fitted WLS line
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=False)
    for ax, isl, tid in zip(axes, ISLANDS, ["T1", "T2"]):
        d = yearly[yearly["island"] == isl]
        m, _ = fit_wls(d, "prop_severe", ["rain_juldec", "year0"], "fire_points")
        # fitted at each year's observed rain
        X = sm.add_constant(d[["rain_juldec", "year0"]])
        fit = m.predict(X)
        ax.scatter(d["year"], d["prop_severe"], s=30, label="observed")
        ax.plot(d["year"], fit, color="red", label="WLS fit")
        ax.set_title(f"{isl} ({tid}): severe-event share 2002-2025")
        ax.set_xlabel("year")
        ax.set_ylabel("share of events that are severe")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(RES, "v2_t1t2_trend.png"), dpi=140)
    plt.close(fig)

    # exploratory: FRP sum vs Jul-Dec rain, scatter + lowess-ish smoother
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, isl in zip(axes, ISLANDS):
        d = yearly[yearly["island"] == isl]
        ax.scatter(d["rain_juldec"], d["frp_sum"], s=30)
        # simple loess via polynomial order 2
        try:
            x = d["rain_juldec"].to_numpy(float)
            y = d["frp_sum"].to_numpy(float)
            order = np.argsort(x)
            xs = x[order]
            coef = np.polyfit(x, y, 2)
            ax.plot(xs, np.polyval(coef, xs), color="red", label="quadratic smoother")
        except Exception:
            pass
        ax.set_title(f"{isl}: Jul-Dec FRP sum vs rain")
        ax.set_xlabel("Jul-Dec rain (mm)")
        ax.set_ylabel("Jul-Dec FRP sum (MW)")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(RES, "v2_exploratory_frp_rain.png"), dpi=140)
    plt.close(fig)


def main():
    os.makedirs(RES, exist_ok=True)
    print("building events 2002-2025 (8-neighbour, all detections)...")
    events, n_used = build_all_events()
    print(f"  detections used: {n_used}; events: {len(events)}")
    pd.DataFrame([{"detections_used": n_used, "events_kept": len(events)}]).to_csv(
        os.path.join(RES, "v2_event_build_summary.csv"), index=False)
    rain = load_rain()
    yearly = yearly_table(events, rain)

    # Step 1 (2002-2019)
    print("Step 1...")
    step1 = run_step1(yearly)
    step1.to_csv(os.path.join(RES, "v2_step1_models.csv"), index=False)
    yearly[yearly["year"].between(2002, 2019)].to_csv(os.path.join(RES, "v2_step1_yearly.csv"), index=False)

    # T1/T2
    print("T1/T2...")
    t1t2 = run_t1t2(yearly)
    t1t2.to_csv(os.path.join(RES, "v2_t1t2_primary.csv"), index=False)
    yearly.to_csv(os.path.join(RES, "v2_t1t2_yearly.csv"), index=False)

    # T1/T2 robustness
    print("T1/T2 robustness...")
    rob = run_t1t2_robustness(yearly, events)
    rob.to_csv(os.path.join(RES, "v2_t1t2_robustness.csv"), index=False)

    # Holm
    print("Holm...")
    h = holm()
    h.to_csv(os.path.join(RES, "v2_holm.csv"), index=False)

    # VIIRS / CHIRPS
    pd.concat([viirs(), chirps()], ignore_index=True).to_csv(
        os.path.join(RES, "v2_viirs_chirps_status.csv"), index=False)

    # exploratory
    print("exploratory...")
    sk, cmp = exploratory(yearly, events)
    sk.to_csv(os.path.join(RES, "v2_exploratory_skewness.csv"), index=False)
    cmp.to_csv(os.path.join(RES, "v2_exploratory_2019_vs_2023.csv"), index=False)

    # plots
    print("plots...")
    make_plots(yearly, events)

    pd.set_option("display.width", 240)
    pd.set_option("display.max_columns", 30)
    print("\n=== Step 1 ===")
    print(step1.to_string(index=False))
    print("\n=== T1/T2 ===")
    print(t1t2.to_string(index=False))
    print("\n=== T1/T2 robustness ===")
    print(rob.to_string(index=False))
    print("\n=== Holm ===")
    print(h.to_string(index=False))


if __name__ == "__main__":
    main()
