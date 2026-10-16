"""Round 2: official ONI cross-check and the Indian Ocean Dipole (DMI).

Inputs
  data/raw/noaa_psl_oni.data          NOAA PSL copy of CPC ONI (ERSST v6), 3-month running mean
  data/raw/noaa_psl_dmi_had_long.data NOAA PSL DMI from HadISST1.1 (preliminary for recent months)
  results/yearly.csv                  round-1 output (SOI, rain, Singapore haze per year)

ONI column convention: in the PSL file each month holds the 3-month mean centred on it
(Jul = JJA, Sep = ASO). Checked against CPC's published season labels: 2015 Dec = NDJ.

Missing-value markers (-99.9, -9999) become NaN. Nothing is filled.
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
RES = sys.argv[2] if len(sys.argv) > 2 else "results"


def read_psl(path, missing):
    """Parse a NOAA PSL year x 12-month text table into a monthly Series."""
    with open(path) as f:
        lines = f.read().splitlines()
    first, last = (int(v) for v in lines[0].split()[:2])
    vals = {}
    for ln in lines[1:]:
        parts = ln.split()
        if len(parts) != 13 or not parts[0].isdigit():
            continue
        y = int(parts[0])
        if not first <= y <= last:
            continue
        for m, v in enumerate(parts[1:], start=1):
            x = float(v)
            vals[pd.Timestamp(y, m, 1)] = np.nan if x <= missing else x
    s = pd.Series(vals).sort_index()
    return s


oni = read_psl(os.path.join(RAW, "noaa_psl_oni.data"), missing=-99.0)
dmi = read_psl(os.path.join(RAW, "noaa_psl_dmi_had_long.data"), missing=-999.0)
soi = pd.read_csv(os.path.join(RES, "soi_monthly.csv"), index_col=0, parse_dates=True).iloc[:, 0]
yr = pd.read_csv(os.path.join(RES, "yearly.csv"), index_col=0)


def mean_months(s, y, months):
    v = [s.get(pd.Timestamp(y, m, 1), np.nan) for m in months]
    return np.nan if any(np.isnan(v)) else float(np.mean(v))


for y in yr.index:
    yr.loc[y, "oni_jja"] = oni.get(pd.Timestamp(y, 7, 1), np.nan)   # JJA centred on Jul
    yr.loc[y, "oni_aso"] = oni.get(pd.Timestamp(y, 9, 1), np.nan)   # ASO centred on Sep
    yr.loc[y, "dmi_jja"] = mean_months(dmi, y, [6, 7, 8])
    yr.loc[y, "dmi_aso"] = mean_months(dmi, y, [8, 9, 10])

rows = []


def corr(df, x, y, label):
    m = df[[x, y]].dropna()
    pr, pp = stats.pearsonr(m[x], m[y])
    sr, sp = stats.spearmanr(m[x], m[y])
    rows.append({"test": label, "x": x, "y": y, "n": len(m), "years": f"{m.index.min()}-{m.index.max()}",
                 "pearson_r": round(pr, 3), "pearson_p": round(pp, 4),
                 "spearman_rho": round(sr, 3), "spearman_p": round(sp, 4)})


def partial(df, x, y, z, label):
    """Partial correlation of x and y controlling for z (residuals of linear fits)."""
    m = df[[x, y, z]].dropna()
    rx = m[x] - np.polyval(np.polyfit(m[z], m[x], 1), m[z])
    ry = m[y] - np.polyval(np.polyfit(m[z], m[y], 1), m[z])
    r, _ = stats.pearsonr(rx, ry)
    n = len(m)
    t = r * np.sqrt((n - 3) / (1 - r ** 2))
    p = 2 * stats.t.sf(abs(t), n - 3)
    rows.append({"test": label, "x": f"{x} | {z}", "y": y, "n": n, "years": f"{m.index.min()}-{m.index.max()}",
                 "pearson_r": round(r, 3), "pearson_p": round(p, 4), "spearman_rho": np.nan, "spearman_p": np.nan})


# 1. SOI vs ONI cross-check (monthly SOI as 3-month centred mean, to match ONI)
soi3 = soi.rolling(3, center=True).mean()
both = pd.concat([soi3.rename("soi3"), oni.rename("oni")], axis=1).dropna()
both = both[(both.index.year >= 1950) & (both.index.year <= 2025)]
both.index = both.index.year * 100 + both.index.month
corr(both, "soi3", "oni", "1: SOI(3-mo) vs ONI, monthly 1950-2025")

full = yr.loc[1950:2025]
corr(full, "soi_aso", "oni_aso", "1: SOI vs ONI, Aug-Oct, yearly")

# 2. Round-1 tests redone with ONI
for x in ["oni_jja", "oni_aso"]:
    for y in ["rain_sumatra_aso", "rain_kalimantan_aso"]:
        corr(full, x, y, "2: ONI -> rain (1950-2025)")
sg = yr.loc[2016:2025]
for x in ["oni_jja", "oni_aso"]:
    for y in ["sg_pm25_mean", "sg_days_psi_over_100"]:
        corr(sg, x, y, "2: ONI -> Singapore haze (2016-2025)")

# 3. IOD
corr(full, "oni_aso", "dmi_aso", "3: ONI vs DMI overlap, Aug-Oct (1950-2025)")
for y in ["rain_sumatra_aso", "rain_kalimantan_aso"]:
    corr(full, "dmi_aso", y, "3: DMI -> rain (1950-2025)")
    partial(full, "dmi_aso", y, "oni_aso", "3: DMI -> rain, ONI held fixed (partial r)")
    partial(full, "oni_aso", y, "dmi_aso", "3: ONI -> rain, DMI held fixed (partial r)")
for y in ["sg_pm25_mean", "sg_days_psi_over_100"]:
    corr(sg, "dmi_aso", y, "3: DMI -> Singapore haze (2016-2025)")

res = pd.DataFrame(rows)
res.to_csv(os.path.join(RES, "correlations_r2.csv"), index=False)

# 4. Two-predictor regression of rain on ONI and DMI (1950-2025), standardised coefficients
reg = []
for y in ["rain_sumatra_aso", "rain_kalimantan_aso"]:
    m = full[["oni_aso", "dmi_aso", y]].dropna()
    Z = (m - m.mean()) / m.std()
    X = np.column_stack([np.ones(len(Z)), Z["oni_aso"], Z["dmi_aso"]])
    beta, *_ = np.linalg.lstsq(X, Z[y], rcond=None)
    fit = X @ beta
    r2 = 1 - ((Z[y] - fit) ** 2).sum() / ((Z[y] - Z[y].mean()) ** 2).sum()
    r2_oni = stats.pearsonr(m["oni_aso"], m[y])[0] ** 2
    reg.append({"y": y, "n": len(m), "beta_oni": round(beta[1], 3), "beta_dmi": round(beta[2], 3),
                "r2_oni_only": round(r2_oni, 3), "r2_oni_plus_dmi": round(r2, 3)})
reg = pd.DataFrame(reg)
reg.to_csv(os.path.join(RES, "regression_r2.csv"), index=False)

# 5. Singapore: residual of PM2.5 after ONI (Jun-Aug), next to DMI, 2016-2025
m = sg[["oni_jja", "sg_pm25_mean", "dmi_aso", "sg_days_psi_over_100"]].dropna()
coef = np.polyfit(m["oni_jja"], m["sg_pm25_mean"], 1)
m = m.assign(pm25_pred_from_oni=np.polyval(coef, m["oni_jja"]))
m["pm25_residual"] = m["sg_pm25_mean"] - m["pm25_pred_from_oni"]
m.round(3).to_csv(os.path.join(RES, "sg_residual_r2.csv"))

yr[["oni_jja", "oni_aso", "dmi_jja", "dmi_aso"]].to_csv(os.path.join(RES, "indices_yearly_r2.csv"))

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 20)
print(res.to_string(index=False))
print()
print(reg.to_string(index=False))
print()
print(m.round(2).to_string())
print()
print("2026:", yr.loc[2026, ["oni_jja", "oni_aso", "dmi_jja", "dmi_aso"]].to_dict())
print("Top DMI Aug-Oct years:", full["dmi_aso"].nlargest(8).round(2).to_dict())
