"""Round 3: is the SOI advantage a shared-ERA5 artefact? Re-test with GPCP rainfall.

GPCP v2.3 monthly (satellite + gauge, 2.5 deg) is independent of ERA5.
For each of the six ERA5 points, the nearest GPCP cell centre is used, then averaged
per island, mirroring the ERA5 design. Aug-Oct mean of monthly rates, mm/day.
Years with any missing month are left blank. GPCP ends Jun 2026, so 1979-2025.

Reads round-1/2 results (yearly.csv, indices_yearly_r2.csv), so run after them.
"""
import os
import sys

import netCDF4 as nc
import numpy as np
import pandas as pd
from scipy import stats

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
RES = sys.argv[2] if len(sys.argv) > 2 else "results"

POINTS = {
    "riau": (0.50, 101.50), "jambi": (-1.60, 103.60), "south_sumatra": (-3.00, 104.80),
    "west_kalimantan": (-0.50, 109.50), "central_kalimantan": (-2.20, 113.90),
    "south_kalimantan": (-3.30, 114.60),
}
SUM = ["riau", "jambi", "south_sumatra"]
KAL = ["west_kalimantan", "central_kalimantan", "south_kalimantan"]

ds = nc.Dataset(os.path.join(RAW, "noaa_psl_gpcp_v2.3_precip.mon.mean.nc"))
lat = np.array(ds.variables["lat"][:])
lon = np.array(ds.variables["lon"][:])
t = ds.variables["time"]
dates = pd.to_datetime([f"{d.year}-{d.month:02d}-01" for d in nc.num2date(t[:], t.units)])
pr = np.ma.filled(ds.variables["precip"][:].astype(float), np.nan)

cells, series = [], {}
for name, (la, lo) in POINTS.items():
    i = int(np.argmin(np.abs(lat - la)))
    j = int(np.argmin(np.abs(lon - lo)))
    cells.append({"point": name, "req_lat": la, "req_lon": lo, "cell_lat": float(lat[i]), "cell_lon": float(lon[j])})
    series[name] = pd.Series(pr[:, i, j], index=dates)
cells = pd.DataFrame(cells)
g = pd.DataFrame(series)


def aso(cols, y):
    s = g.loc[(g.index.year == y) & g.index.month.isin([8, 9, 10]), cols]
    if len(s) != 3 or s.isna().any().any():
        return np.nan
    return float(s.mean(axis=1).mean())


yr = pd.read_csv(os.path.join(RES, "yearly.csv"), index_col=0)
idx = pd.read_csv(os.path.join(RES, "indices_yearly_r2.csv"), index_col=0)
yr = yr.join(idx)
for y in yr.index:
    yr.loc[y, "gpcp_sumatra_aso"] = aso(SUM, y)
    yr.loc[y, "gpcp_kalimantan_aso"] = aso(KAL, y)
yr[["gpcp_sumatra_aso", "gpcp_kalimantan_aso"]].to_csv(os.path.join(RES, "gpcp_yearly_r3.csv"))
cells.to_csv(os.path.join(RES, "gpcp_cells_r3.csv"), index=False)

rows = []


def corr(df, x, y, label):
    m = df[[x, y]].dropna()
    pr_, pp = stats.pearsonr(m[x], m[y])
    sr, sp = stats.spearmanr(m[x], m[y])
    rows.append({"test": label, "x": x, "y": y, "n": len(m), "years": f"{m.index.min()}-{m.index.max()}",
                 "pearson_r": round(pr_, 3), "pearson_p": round(pp, 4),
                 "spearman_rho": round(sr, 3), "spearman_p": round(sp, 4)})


def partial(df, x, y, z, label):
    m = df[[x, y, z]].dropna()
    rx = m[x] - np.polyval(np.polyfit(m[z], m[x], 1), m[z])
    ry = m[y] - np.polyval(np.polyfit(m[z], m[y], 1), m[z])
    r, _ = stats.pearsonr(rx, ry)
    n = len(m)
    tval = r * np.sqrt((n - 3) / (1 - r ** 2))
    p = 2 * stats.t.sf(abs(tval), n - 3)
    rows.append({"test": label, "x": f"{x} | {z}", "y": y, "n": n, "years": f"{m.index.min()}-{m.index.max()}",
                 "pearson_r": round(r, 3), "pearson_p": round(p, 4), "spearman_rho": np.nan, "spearman_p": np.nan})


common = yr.loc[1979:2025]

# 1. Do the two rainfall records agree?
corr(common, "rain_sumatra_aso", "gpcp_sumatra_aso", "1: ERA5 vs GPCP rain, Aug-Oct")
corr(common, "rain_kalimantan_aso", "gpcp_kalimantan_aso", "1: ERA5 vs GPCP rain, Aug-Oct")

# 2. SOI and ONI against both rain records, same years (1979-2025)
for isl in ["sumatra", "kalimantan"]:
    for src, col in [("ERA5", f"rain_{isl}_aso"), ("GPCP", f"gpcp_{isl}_aso")]:
        corr(common, "soi_aso", col, f"2: SOI -> rain ({src})")
        corr(common, "oni_aso", col, f"2: ONI -> rain ({src})")

# 3. Bootstrap the gap |r_SOI| - |r_ONI| for each rain source (paired resampling of years)
rng = np.random.default_rng(20261016)
boot = []
for isl in ["sumatra", "kalimantan"]:
    for src, col in [("ERA5", f"rain_{isl}_aso"), ("GPCP", f"gpcp_{isl}_aso")]:
        m = common[["soi_aso", "oni_aso", col]].dropna().to_numpy()
        n = len(m)
        gap0 = abs(np.corrcoef(m[:, 0], m[:, 2])[0, 1]) - abs(np.corrcoef(m[:, 1], m[:, 2])[0, 1])
        gaps = []
        for _ in range(10000):
            s = m[rng.integers(0, n, n)]
            gaps.append(abs(np.corrcoef(s[:, 0], s[:, 2])[0, 1]) - abs(np.corrcoef(s[:, 1], s[:, 2])[0, 1]))
        lo, hi = np.percentile(gaps, [2.5, 97.5])
        boot.append({"island": isl, "rain": src, "n": n, "gap_abs_r_soi_minus_oni": round(gap0, 3),
                     "ci95_low": round(lo, 3), "ci95_high": round(hi, 3)})
boot = pd.DataFrame(boot)
boot.to_csv(os.path.join(RES, "soi_oni_gap_bootstrap_r3.csv"), index=False)

# 4. IOD with GPCP
for isl in ["sumatra", "kalimantan"]:
    col = f"gpcp_{isl}_aso"
    corr(common, "dmi_aso", col, "4: DMI -> rain (GPCP)")
    partial(common, "dmi_aso", col, "oni_aso", "4: DMI -> rain (GPCP), ONI held fixed")
    # same years with ERA5, for a like-for-like comparison with round 2 (which used 1950-2025)
    partial(common, "dmi_aso", f"rain_{isl}_aso", "oni_aso", "4: DMI -> rain (ERA5, 1979-2025), ONI held fixed")

# 5. GPCP rain -> Singapore haze, 2016-2025
sg = yr.loc[2016:2025]
for isl in ["sumatra", "kalimantan"]:
    for y in ["sg_pm25_mean", "sg_days_psi_over_100"]:
        corr(sg, f"gpcp_{isl}_aso", y, "5: GPCP rain -> Singapore haze (2016-2025)")

res = pd.DataFrame(rows)
res.to_csv(os.path.join(RES, "correlations_r3.csv"), index=False)

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 20)
print(cells.to_string(index=False))
print()
print(res.to_string(index=False))
print()
print(boot.to_string(index=False))
print()
print(yr.loc[[1982, 1997, 2006, 2015, 2019, 2023, 2025], ["rain_kalimantan_aso", "gpcp_kalimantan_aso",
                                                           "rain_sumatra_aso", "gpcp_sumatra_aso"]].round(2))
