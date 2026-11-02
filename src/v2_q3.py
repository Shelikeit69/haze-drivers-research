"""Plan v2, Q3: v1 H3 re-run with Sloan's two suggestions (docs/research_plan_v2.md).

Primary tests (unadjusted p here; Holm over T1-T6 once T1-T2 exist):
  T3/T4  log10(Aug-Oct FRP sum) ~ GPCP Aug-Oct mean rain (mm/day) + post2016, 2002-2025
  T5/T6  log10(Aug-Oct FRP sum) ~ GPCP Jun-Oct total rain (mm) + post2016, 2002-2025
Robustness (plan items 1-5 and 7; CHIRPS and VIIRS not yet available):
  log rain; Jul-Oct total; linear trend instead of step; moving-block bootstrap (3 years);
  leave-one-year-out; Aqua-only FRP; Singapore PM2.5 vs FRP sum (Spearman, 2016-2025).
Reference rows: v1 H3 (detection counts, Aug-Oct GPCP) on the same 2002-2025 sample.

Usage: python src/v2_q3.py data/raw results
"""
import glob
import os
import sys

import netCDF4 as nc
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
RES = sys.argv[2] if len(sys.argv) > 2 else "results"
YEARS = (2002, 2025)
SEED = 20261102
B = 10000
ISL = ["sumatra", "kalimantan"]

# ---------- rain: GPCP v2.3, the three v1 cells per island ----------
cells = pd.read_csv(os.path.join(RES, "gpcp_cells_r3.csv")).set_index("point")
GROUP = {"sumatra": ["riau", "jambi", "south_sumatra"],
         "kalimantan": ["west_kalimantan", "central_kalimantan", "south_kalimantan"]}
ds = nc.Dataset(os.path.join(RAW, "noaa_psl_gpcp_v2.3_precip.mon.mean.nc"))
lat = np.array(ds.variables["lat"][:])
lon = np.array(ds.variables["lon"][:])
t = ds.variables["time"]
dates = pd.to_datetime([f"{d.year}-{d.month:02d}-01" for d in nc.num2date(t[:], t.units)])
pr = np.ma.filled(ds.variables["precip"][:].astype(float), np.nan)  # mm/day, monthly mean
ser = {}
for p, r in cells.iterrows():
    i = int(np.where(np.isclose(lat, r["cell_lat"]))[0][0])
    j = int(np.where(np.isclose(lon, r["cell_lon"]))[0][0])
    ser[p] = pd.Series(pr[:, i, j], index=dates)
g = pd.DataFrame(ser)
days = g.index.days_in_month


def rain(isl, y, months, total):
    s = g.loc[(g.index.year == y) & g.index.month.isin(months), GROUP[isl]]
    if len(s) != len(months) or s.isna().any().any():
        return np.nan
    m = s.mean(axis=1)  # island mean, mm/day per month
    if total:
        return float((m * days[(g.index.year == y) & g.index.month.isin(months)]).sum())
    return float(m.mean())


# ---------- fires ----------
fc = pd.read_csv(os.path.join(RES, "fire_counts_r4.csv"))
fc = fc[fc["source"] == "MODIS_SP"]


def island(la, lo):  # same boxes as src/analyse_r4.py
    if 100 <= lo <= 106.5 and -5 <= la <= 1.0:
        return "sumatra"
    if 100 <= lo <= 101.9 and 1.0 < la <= 2.3:
        return "sumatra"
    if 108.5 <= lo <= 116.5 and -4.5 <= la <= 1.0:
        return "kalimantan"
    return "other"


# Aqua-only Aug-Oct FRP sum from the raw v1 files (robustness 5)
fr = []
for p in sorted(glob.glob(os.path.join(RAW, "firms", "MODIS_SP_*.csv"))):
    d = pd.read_csv(p)
    if d.empty:
        continue
    fr.append(d)
fr = pd.concat(fr, ignore_index=True).drop_duplicates()
fr["acq_date"] = pd.to_datetime(fr["acq_date"])
fr = fr[fr["acq_date"].dt.month.isin([8, 9, 10])]
fr["island"] = [island(a, b) for a, b in zip(fr["latitude"], fr["longitude"])]
fr["year"] = fr["acq_date"].dt.year
aqua = fr[(fr["satellite"] == "Aqua") & (fr["island"] != "other")].groupby(["year", "island"])["frp"].sum()
allsat = fr[fr["island"] != "other"].groupby(["year", "island"])["frp"].sum()

yr4 = pd.read_csv(os.path.join(RES, "yearly_r4.csv"), index_col=0)
rows = []
for y in range(YEARS[0], YEARS[1] + 1):
    row = {"year": y, "post2016": int(y >= 2016), "sg_pm25_mean": yr4.loc[y, "sg_pm25_mean"]}
    for isl in ISL:
        f = fc[(fc["year"] == y) & (fc["island"] == isl)].iloc[0]
        row[f"frp_{isl}"] = f["frp_sum_mw"]
        row[f"frp_check_{isl}"] = round(float(allsat.get((y, isl), np.nan)), 1)
        row[f"frp_aqua_{isl}"] = round(float(aqua.get((y, isl), np.nan)), 1)
        row[f"n_all_{isl}"] = f["n_all"]
        row[f"rain_aso_{isl}"] = rain(isl, y, [8, 9, 10], total=False)
        row[f"rain_junoct_{isl}"] = rain(isl, y, [6, 7, 8, 9, 10], total=True)
        row[f"rain_juloct_{isl}"] = rain(isl, y, [7, 8, 9, 10], total=True)
    rows.append(row)
d = pd.DataFrame(rows).set_index("year")
d["year"] = d.index
for isl in ISL:
    d[f"lfrp_{isl}"] = np.log10(d[f"frp_{isl}"])
    d[f"lfrp_aqua_{isl}"] = np.log10(d[f"frp_aqua_{isl}"])
    d[f"lcount_{isl}"] = np.log10(d[f"n_all_{isl}"])
    for r in ["aso", "junoct", "juloct"]:
        d[f"lograin_{r}_{isl}"] = np.log(d[f"rain_{r}_{isl}"])
d["frp_both"] = d["frp_sumatra"] + d["frp_kalimantan"]
d.to_csv(os.path.join(RES, "v2_q3_yearly.csv"))

# consistency check: FRP sums rebuilt from raw files must match fire_counts_r4.csv
for isl in ISL:
    gap = (d[f"frp_{isl}"] - d[f"frp_check_{isl}"]).abs().max()
    assert gap < 1.0, f"FRP rebuild mismatch {isl}: {gap}"


# ---------- estimation ----------
def coef(df, yv, xs, target):
    m = sm.OLS(df[yv], sm.add_constant(df[xs])).fit()
    return float(m.params[target]), float(m.bse[target]), float(m.pvalues[target])


rng = np.random.default_rng(SEED)


def boot(df, yv, xs, target, block=1):
    n = len(df)
    vals, skipped = [], 0
    for _ in range(B):
        if block == 1:
            idx = rng.integers(0, n, n)
        else:
            starts = rng.integers(0, n - block + 1, int(np.ceil(n / block)))
            idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        s = df.iloc[idx]
        if (s[[yv] + xs].nunique() < 2).any():
            skipped += 1
            continue
        X = np.column_stack([np.ones(n), s[xs].to_numpy(float)])
        beta = np.linalg.lstsq(X, s[yv].to_numpy(float), rcond=None)[0]
        vals.append(beta[1 + xs.index(target)])  # same OLS estimate as coef(), faster
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return lo, hi, skipped


def loo(df, yv, xs, target):
    v = [coef(df.drop(index=y), yv, xs, target) for y in df.index]
    return min(x[0] for x in v), max(x[0] for x in v), max(x[2] for x in v)


def run(tid, kind, desc, yv, xs, target, block=1, do_loo=False):
    df = d[[yv] + xs].dropna()
    b, se, p = coef(df, yv, xs, target)
    lo, hi, sk = boot(df, yv, xs, target, block)
    out = {"id": tid, "kind": kind, "model": desc, "n": len(df),
           "years": f"{df.index.min()}-{df.index.max()}", "coef": b, "se": se, "p_raw": p,
           "boot95_low": lo, "boot95_high": hi, "boot_block": block, "boot_skipped": sk}
    if do_loo:
        out["loo_coef_min"], out["loo_coef_max"], out["loo_max_p"] = loo(df, yv, xs, target)
    return out


res = []
for isl, (ta, tc) in zip(ISL, [("T3", "T5"), ("T4", "T6")]):
    aso, jo = f"rain_aso_{isl}", f"rain_junoct_{isl}"
    y = f"lfrp_{isl}"
    res.append(run(ta, "primary", f"log10 FRP {isl} ~ Aug-Oct rain + post2016", y, [aso, "post2016"], aso, do_loo=True))
    res.append(run(tc, "primary", f"log10 FRP {isl} ~ Jun-Oct total rain + post2016", y, [jo, "post2016"], jo, do_loo=True))
    # robustness
    res.append(run(ta, "rob1 log rain", f"log10 FRP {isl} ~ ln(Aug-Oct rain) + post2016", y,
                   [f"lograin_aso_{isl}", "post2016"], f"lograin_aso_{isl}"))
    res.append(run(tc, "rob1 log rain", f"log10 FRP {isl} ~ ln(Jun-Oct total) + post2016", y,
                   [f"lograin_junoct_{isl}", "post2016"], f"lograin_junoct_{isl}"))
    res.append(run(tc, "rob1 Jul-Oct", f"log10 FRP {isl} ~ Jul-Oct total rain + post2016", y,
                   [f"rain_juloct_{isl}", "post2016"], f"rain_juloct_{isl}"))
    res.append(run(ta, "rob2 linear trend", f"log10 FRP {isl} ~ Aug-Oct rain + year", y, [aso, "year"], aso))
    res.append(run(tc, "rob2 linear trend", f"log10 FRP {isl} ~ Jun-Oct total rain + year", y, [jo, "year"], jo))
    res.append(run(ta, "rob3 block bootstrap", f"log10 FRP {isl} ~ Aug-Oct rain + post2016", y, [aso, "post2016"], aso, block=3))
    res.append(run(tc, "rob3 block bootstrap", f"log10 FRP {isl} ~ Jun-Oct total rain + post2016", y, [jo, "post2016"], jo, block=3))
    res.append(run(ta, "rob5 Aqua only", f"log10 Aqua FRP {isl} ~ Aug-Oct rain + post2016", f"lfrp_aqua_{isl}", [aso, "post2016"], aso))
    res.append(run(tc, "rob5 Aqua only", f"log10 Aqua FRP {isl} ~ Jun-Oct total rain + post2016", f"lfrp_aqua_{isl}", [jo, "post2016"], jo))
    # context: post2016 step in the primary models, and v1 H3 (counts) on the same sample
    res.append(run(ta, "context post2016 step", f"post2016 coef, log10 FRP {isl} ~ Aug-Oct rain + post2016", y, [aso, "post2016"], "post2016"))
    res.append(run(tc, "context post2016 step", f"post2016 coef, log10 FRP {isl} ~ Jun-Oct total rain + post2016", y, [jo, "post2016"], "post2016"))
    res.append(run("v1H3", "reference counts", f"log10 counts {isl} ~ Aug-Oct rain + post2016", f"lcount_{isl}", [aso, "post2016"], aso))
    res.append(run("v1H3", "reference counts", f"log10 counts {isl} ~ Jun-Oct total rain + post2016", f"lcount_{isl}", [jo, "post2016"], jo))
out = pd.DataFrame(res)

# robustness 7: Singapore PM2.5 vs FRP sum, Spearman, 2016-2025
s = d.loc[2016:2025, ["sg_pm25_mean", "frp_both"]].dropna()
rho, p = stats.spearmanr(s["frp_both"], s["sg_pm25_mean"])
out = pd.concat([out, pd.DataFrame([{"id": "H4", "kind": "rob7 FRP instead of counts",
                                     "model": "Spearman FRP sum (both islands) vs Singapore PM2.5",
                                     "n": len(s), "years": f"{s.index.min()}-{s.index.max()}",
                                     "coef": rho, "p_raw": p}])], ignore_index=True)

# readable effect sizes: factor change in FRP for less rain
def factor(r):
    if r["id"] == "H4" or "post2016" in r["model"] and r["kind"].startswith("context"):
        return np.nan
    unit = 1.0 if ("Aug-Oct rain" in r["model"] and "ln(" not in r["model"]) else (100.0 if "total rain" in r["model"] else np.nan)
    return 10 ** (-r["coef"] * unit) if np.isfinite(unit) else np.nan


out["factor_less_rain"] = out.apply(factor, axis=1)
out["factor_unit"] = np.where(out["model"].str.contains("Aug-Oct rain") & ~out["model"].str.contains(r"ln\("),
                              "per 1 mm/day less", np.where(out["model"].str.contains("total rain"), "per 100 mm less", ""))
out.loc[out["kind"].str.startswith("context"), "factor_unit"] = ""  # step rows have no rain-unit factor
out.loc[out["kind"].str.startswith("context"), "factor_post2016"] = 10 ** out.loc[out["kind"].str.startswith("context"), "coef"]
out.to_csv(os.path.join(RES, "v2_q3_results.csv"), index=False)
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 30)
print(out[["id", "kind", "model", "n", "coef", "p_raw", "boot95_low", "boot95_high",
           "factor_less_rain", "factor_unit", "factor_post2016"]].round(4).to_string())
print(out[out["kind"] == "primary"][["id", "loo_coef_min", "loo_coef_max", "loo_max_p"]].to_string())
