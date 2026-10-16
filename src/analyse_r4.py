"""Round 4: fires. Does drought turn into fires, and do fires explain Singapore haze?

Input: data/raw/firms/*.csv (MODIS active fire detections, raw), plus results from rounds 1-3.

Island classification (fixed boxes, applied here so raw files stay untouched):
  Sumatra    = lon 100-106.5, lat -5 to 1.0,  plus lon 100-101.9, lat 1.0-2.3 (northern Riau
               mainland; keeps Peninsular Malaysia, Singapore and Batam/Bintan out).
               Includes Bangka island (lon ~105-106.5), which cannot be split off with a box.
  Kalimantan = lon 108.5-116.5, lat -4.5 to 1.0 (keeps most of Sarawak out).
Everything else in the download box is dropped and counted as "other".

Counts:
  - SP years (2001-2025): all detections, and type == 0 ("presumed vegetation fire").
  - NRT (2026) has no "type" column, so the like-for-like series is "all detections".
  - High-confidence sensitivity: confidence >= 80.
Windows: Aug-Oct (2001-2025) and 1 Aug-10 Oct (2016-2026, matches round-1 window for 2026).
"""
import glob
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
RES = sys.argv[2] if len(sys.argv) > 2 else "results"

frames = []
for p in sorted(glob.glob(os.path.join(RAW, "firms", "*.csv"))):
    df = pd.read_csv(p)
    if df.empty:
        continue
    df["source"] = os.path.basename(p).split("_20")[0]
    frames.append(df)
f = pd.concat(frames, ignore_index=True)
f = f.drop_duplicates()  # guard against any overlap between request windows
f["acq_date"] = pd.to_datetime(f["acq_date"])


def island(lat, lon):
    if 100 <= lon <= 106.5 and -5 <= lat <= 1.0:
        return "sumatra"
    if 100 <= lon <= 101.9 and 1.0 < lat <= 2.3:
        return "sumatra"
    if 108.5 <= lon <= 116.5 and -4.5 <= lat <= 1.0:
        return "kalimantan"
    return "other"


f["island"] = [island(a, b) for a, b in zip(f["latitude"], f["longitude"])]
f["year"] = f["acq_date"].dt.year
f["conf_num"] = pd.to_numeric(f["confidence"], errors="coerce")
f["in_window"] = f["acq_date"].dt.strftime("%m-%d") <= "10-10"

rows = []
for (y, isl), g in f[f["island"] != "other"].groupby(["year", "island"]):
    row = {"year": y, "island": isl, "source": ",".join(sorted(g["source"].unique())),
           "n_all": len(g), "n_all_window": int(g["in_window"].sum()),
           "n_conf80": int((g["conf_num"] >= 80).sum()),
           "frp_sum_mw": round(float(g["frp"].sum()), 1)}
    row["n_type0"] = int((g["type"] == 0).sum()) if "type" in g and g["type"].notna().any() else np.nan
    rows.append(row)
counts = pd.DataFrame(rows)
counts.to_csv(os.path.join(RES, "fire_counts_r4.csv"), index=False)
other = f[f["island"] == "other"].groupby("year").size().rename("n_other")
type_share = f[(f["island"] != "other") & f["type"].notna()].groupby("year")["type"].apply(lambda s: round(float((s != 0).mean()), 4))

wide = counts.pivot(index="year", columns="island", values=["n_all", "n_all_window", "n_type0", "n_conf80"])
wide.columns = [f"{a}_{b}" for a, b in wide.columns]

yr = pd.read_csv(os.path.join(RES, "yearly.csv"), index_col=0)
yr = yr.join(pd.read_csv(os.path.join(RES, "indices_yearly_r2.csv"), index_col=0))
yr = yr.join(pd.read_csv(os.path.join(RES, "gpcp_yearly_r3.csv"), index_col=0))
yr = yr.join(wide)
for isl in ["sumatra", "kalimantan"]:
    yr[f"log_fires_{isl}"] = np.log10(yr[f"n_all_{isl}"])
    yr[f"log_fires_w_{isl}"] = np.log10(yr[f"n_all_window_{isl}"])
yr["log_fires_both"] = np.log10(yr["n_all_sumatra"] + yr["n_all_kalimantan"])
yr.to_csv(os.path.join(RES, "yearly_r4.csv"))

out = []


def corr(df, x, y, label):
    m = df[[x, y]].dropna()
    pr, pp = stats.pearsonr(m[x], m[y])
    sr, sp = stats.spearmanr(m[x], m[y])
    out.append({"test": label, "x": x, "y": y, "n": len(m), "years": f"{m.index.min()}-{m.index.max()}",
                "pearson_r": round(pr, 3), "pearson_p": round(pp, 4),
                "spearman_rho": round(sr, 3), "spearman_p": round(sp, 4)})


sp = yr.loc[2001:2025]
for isl in ["sumatra", "kalimantan"]:
    corr(sp, f"gpcp_{isl}_aso", f"log_fires_{isl}", "1: GPCP rain -> log10 fires, Aug-Oct")
    corr(sp, "oni_aso", f"log_fires_{isl}", "1: ONI -> log10 fires, Aug-Oct")
    corr(sp, "oni_jja", f"log_fires_{isl}", "1: ONI Jun-Aug (lead) -> log10 fires")
sg = yr.loc[2016:2025]
for x in ["log_fires_sumatra", "log_fires_kalimantan", "log_fires_both"]:
    corr(sg, x, "sg_pm25_mean", "2: log10 fires -> Singapore PM2.5, Aug-Oct (2016-2025)")
sgw = yr.loc[2016:2026]
for x in ["log_fires_w_sumatra", "log_fires_w_kalimantan"]:
    corr(sgw, x, "w_sg_pm25_mean", "2: log10 fires -> Singapore PM2.5, 1 Aug-10 Oct incl. 2026")
res = pd.DataFrame(out)
res.to_csv(os.path.join(RES, "correlations_r4.csv"), index=False)

# Threshold view: fires in years with GPCP Aug-Oct rain below vs above 4 mm/day (descriptive only)
thr = []
for isl in ["sumatra", "kalimantan"]:
    m = sp[[f"gpcp_{isl}_aso", f"n_all_{isl}"]].dropna()
    dry = m[m[f"gpcp_{isl}_aso"] < 4]
    wet = m[m[f"gpcp_{isl}_aso"] >= 4]
    thr.append({"island": isl, "dry_years": len(dry), "dry_median_fires": float(dry[f"n_all_{isl}"].median()),
                "wet_years": len(wet), "wet_median_fires": float(wet[f"n_all_{isl}"].median()),
                "dry_list": ";".join(str(i) for i in dry.index)})
thr = pd.DataFrame(thr)
thr.to_csv(os.path.join(RES, "fire_rain_threshold_r4.csv"), index=False)

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 30)
print(res.to_string(index=False))
print()
print(thr.to_string(index=False))
print()
cols = ["n_all_sumatra", "n_all_kalimantan", "n_type0_sumatra", "n_type0_kalimantan",
        "n_all_window_sumatra", "n_all_window_kalimantan", "gpcp_sumatra_aso", "gpcp_kalimantan_aso",
        "sg_pm25_mean", "w_sg_pm25_mean"]
print(yr.loc[2001:2026, cols].round(2).to_string())
print()
print("other (dropped) per year, min/max:", int(other.min()), int(other.max()))
print("share of non-type-0 among island detections, SP years, max:", float(type_share.max()))
