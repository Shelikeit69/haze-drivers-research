"""El Nino vs Indonesian dry-season rain vs Singapore haze.

ENSO index: Southern Oscillation Index (Troup method) computed from ERA5 monthly
mean sea-level pressure at Tahiti and Darwin, base period 1981-2010.
Negative SOI = El Nino-like.

Outputs: results/*.csv and printed tables. No smoothing, no gap filling.
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
RES = sys.argv[2] if len(sys.argv) > 2 else "results"
os.makedirs(RES, exist_ok=True)


def load_era5(name):
    with open(os.path.join(RAW, f"era5_{name}.json")) as f:
        d = json.load(f)["daily"]
    df = pd.DataFrame(d)
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")


# ---------- SOI ----------
dar = load_era5("darwin")["pressure_msl_mean"].resample("MS").mean()
tah = load_era5("tahiti")["pressure_msl_mean"].resample("MS").mean()
diff = (tah - dar).dropna()
base = diff["1981":"2010"]
clim = base.groupby(base.index.month).mean()
sd = base.groupby(base.index.month).std()
soi = 10 * (diff - clim.reindex(diff.index.month).values) / sd.reindex(diff.index.month).values
soi.name = "soi"
soi.to_csv(os.path.join(RES, "soi_monthly.csv"))


def season_mean(series, months, year):
    s = series[(series.index.year == year) & (series.index.month.isin(months))]
    return s.mean() if len(s) == len(months) else np.nan


# ---------- rainfall ----------
SUM = ["riau", "jambi", "south_sumatra"]
KAL = ["west_kalimantan", "central_kalimantan", "south_kalimantan"]
rain = {}
for n in SUM + KAL:
    r = load_era5(n)["precipitation_sum"]
    rain[n] = r
rain = pd.DataFrame(rain)

years = range(1950, 2027)
rows = []
for y in years:
    sub = rain[(rain.index.year == y) & (rain.index.month.isin([8, 9, 10]))]
    complete = len(sub) == 92 and sub.notna().all().all()
    rows.append({
        "year": y,
        "soi_jja": season_mean(soi, [6, 7, 8], y),
        "soi_aso": season_mean(soi, [8, 9, 10], y),
        "rain_sumatra_aso": sub[SUM].mean(axis=1).mean() if complete else np.nan,
        "rain_kalimantan_aso": sub[KAL].mean(axis=1).mean() if complete else np.nan,
        "rain_days_aso": len(sub),
    })
yr = pd.DataFrame(rows).set_index("year")

# ---------- Singapore haze ----------
recs = []
for p in sorted(glob.glob(os.path.join(RAW, "psi", "*.json"))):
    with open(p) as f:
        j = json.load(f)
    if j.get("code") != 0 or not j.get("data"):
        continue
    # The "national" field disappears from 2024, so both metrics are rebuilt from the
    # five regions for every year: PSI = max over regions (NEA's national definition),
    # PM2.5 = mean over the regions reporting at that hour.
    REG = ["north", "south", "east", "west", "central"]
    for it in j["data"]["items"]:
        rd = it["readings"]
        psi = [rd.get("psi_twenty_four_hourly", {}).get(r) for r in REG]
        pm = [rd.get("pm25_twenty_four_hourly", {}).get(r) for r in REG]
        psi = [v for v in psi if v is not None]
        pm = [v for v in pm if v is not None]
        recs.append({
            "ts": it["timestamp"],
            "psi24": max(psi) if psi else None,
            "pm25_24": float(np.mean(pm)) if pm else None,
        })
h = pd.DataFrame(recs)
h["ts"] = pd.to_datetime(h["ts"], utc=True).dt.tz_convert("Asia/Singapore")
h["date"] = h["ts"].dt.date
daily = h.groupby("date").agg(psi24_max=("psi24", "max"), pm25_24_mean=("pm25_24", "mean"),
                              n_hours=("psi24", "count"))
daily.index = pd.to_datetime(daily.index)
daily.to_csv(os.path.join(RES, "sg_daily_aug_oct.csv"))

hz = []
for y in range(2016, 2027):
    d = daily[daily.index.year == y]
    hz.append({
        "year": y,
        "sg_days_with_data": len(d),
        "sg_pm25_mean": d["pm25_24_mean"].mean(),
        "sg_days_psi_over_100": int((d["psi24_max"] > 100).sum()),
        "sg_psi24_max": d["psi24_max"].max(),
    })
hz = pd.DataFrame(hz).set_index("year")
yr = yr.join(hz)

# Same-window comparison that can include 2026: 1 Aug - 10 Oct (rain data ends ~10 Oct 2026)
win = []
for y in range(2016, 2027):
    lo, hi = pd.Timestamp(y, 8, 1), pd.Timestamp(y, 10, 10)
    r = rain[(rain.index >= lo) & (rain.index <= hi)]
    d = daily[(daily.index >= lo) & (daily.index <= hi)]
    ok = len(r) == 71 and r.notna().all().all()
    win.append({"year": y,
                "w_rain_sumatra": r[SUM].mean(axis=1).mean() if ok else np.nan,
                "w_rain_kalimantan": r[KAL].mean(axis=1).mean() if ok else np.nan,
                "w_sg_days": len(d),
                "w_sg_pm25_mean": d["pm25_24_mean"].mean(),
                "w_sg_days_psi_over_100": int((d["psi24_max"] > 100).sum())})
yr = yr.join(pd.DataFrame(win).set_index("year"))
yr.to_csv(os.path.join(RES, "yearly.csv"))


def corr(x, y, label):
    m = yr[[x, y]].dropna()
    pr, pp = stats.pearsonr(m[x], m[y])
    sr, sp = stats.spearmanr(m[x], m[y])
    return {"test": label, "x": x, "y": y, "n": len(m), "years": f"{m.index.min()}-{m.index.max()}",
            "pearson_r": round(pr, 3), "pearson_p": round(pp, 4),
            "spearman_rho": round(sr, 3), "spearman_p": round(sp, 4)}


full = yr.loc[1950:2025]
out = []
yr_bak = yr
yr = full
for x in ["soi_jja", "soi_aso"]:
    for y in ["rain_sumatra_aso", "rain_kalimantan_aso"]:
        out.append(corr(x, y, "A: ENSO -> rain (1950-2025)"))
yr = yr_bak.loc[2016:2025]
for x in ["soi_jja", "soi_aso", "rain_sumatra_aso", "rain_kalimantan_aso"]:
    for y in ["sg_pm25_mean", "sg_days_psi_over_100"]:
        out.append(corr(x, y, "B: -> Singapore haze (2016-2025)"))
yr = yr_bak.loc[2016:2026]
for x in ["soi_jja", "w_rain_sumatra", "w_rain_kalimantan"]:
    for y in ["w_sg_pm25_mean", "w_sg_days_psi_over_100"]:
        out.append(corr(x, y, "C: same window 1 Aug-10 Oct, incl. 2026"))
yr = yr_bak
res = pd.DataFrame(out)
res.to_csv(os.path.join(RES, "correlations.csv"), index=False)

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
print(res.to_string(index=False))
print()
print(yr.loc[2014:2026].round(2).T.to_string())
