"""Share of August-October MODIS fire detections by month, 2001-2025 (MODIS_SP),
for both island boxes combined (100-116.5E, 5S-1N; a simple box used only for this share).

Output: results/fire_month_share.csv
"""
import glob
import os
import sys

import pandas as pd

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
RES = sys.argv[2] if len(sys.argv) > 2 else "results"

f = pd.concat([pd.read_csv(p, usecols=["latitude", "longitude", "acq_date"])
               for p in sorted(glob.glob(os.path.join(RAW, "firms", "MODIS_SP_*.csv")))])
f = f[f["longitude"].between(100, 116.5) & f["latitude"].between(-5, 1)]
f["month"] = f["acq_date"].str[5:7]
f["year"] = f["acq_date"].str[:4]
share = f.groupby("month").size() / len(f)
by_year = f.groupby(["year", "month"]).size().unstack()
out = pd.DataFrame({"share_of_aug_oct_detections": share.round(4)})
out.loc["years_aug_largest", "share_of_aug_oct_detections"] = int((by_year.idxmax(axis=1) == "08").sum())
out.to_csv(os.path.join(RES, "fire_month_share.csv"))
print(out)
