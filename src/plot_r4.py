"""Round 4 figure: rain vs fires (2001-2025) and fires vs Singapore PM2.5 (2016-2026)."""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RES = sys.argv[1] if len(sys.argv) > 1 else "results"
y = pd.read_csv(f"{RES}/yearly_r4.csv", index_col=0)

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#1f1f1e", "#6b6a63", "#e6e5df"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED})
fig, axes = plt.subplots(2, 1, figsize=(6.4, 9.6))

a = axes[0]
d = y.loc[2001:2025]
a.scatter(d["gpcp_kalimantan_aso"], d["n_all_kalimantan"], s=48, color=BLUE, edgecolor="white",
          linewidth=1.2, zorder=3, label="Kalimantan")
a.scatter(d["gpcp_sumatra_aso"], d["n_all_sumatra"], s=48, color=ORANGE, edgecolor="white",
          linewidth=1.2, zorder=3, label="Sumatra")
a.set_yscale("log")
a.axvline(4, color=MUTED, linewidth=1, linestyle="--", zorder=1)
a.text(4.1, 700, "4 mm/day", color=MUTED, fontsize=9)
for yr_, isl, off in [(2015, "kalimantan", (4, -14)), (2006, "kalimantan", (6, 2)), (2019, "sumatra", (6, 2)),
                      (2023, "sumatra", (6, -10)), (2022, "kalimantan", (-14, 8))]:
    a.annotate(str(yr_), (d.loc[yr_, f"gpcp_{isl}_aso"], d.loc[yr_, f"n_all_{isl}"]), xytext=off,
               textcoords="offset points", color=INK, fontsize=9)
a.set_title("Aug–Oct rain vs fire detections, 2001–2025", loc="left", color=INK, fontsize=12)
a.set_xlabel("Rain, mm/day (GPCP)")
a.set_ylabel("MODIS fire detections (log scale)")
a.legend(frameon=False, loc="upper right")

a = axes[1]
d = y.loc[2016:2026].copy()
d["fires"] = d["n_all_window_sumatra"] + d["n_all_window_kalimantan"]
b = d.drop(index=2026)
a.scatter(b["fires"], b["w_sg_pm25_mean"], s=56, color=BLUE, edgecolor="white", linewidth=1.2, zorder=3)
a.scatter([d.loc[2026, "fires"]], [d.loc[2026, "w_sg_pm25_mean"]], s=70, color=ORANGE, edgecolor="white",
          linewidth=1.2, zorder=4)
offs = {2017: (6, -12), 2021: (6, -10), 2020: (6, 2), 2022: (-30, 4), 2025: (6, 4), 2024: (6, -10)}
for yr_ in d.index:
    a.annotate(str(yr_), (d.loc[yr_, "fires"], d.loc[yr_, "w_sg_pm25_mean"]), xytext=offs.get(yr_, (6, 4)),
               textcoords="offset points", color=INK, fontsize=9)
a.set_xscale("log")
from matplotlib.ticker import NullFormatter, FixedLocator, FixedFormatter
a.xaxis.set_minor_formatter(NullFormatter())
a.xaxis.set_major_locator(FixedLocator([2000, 5000, 10000, 20000, 50000]))
a.xaxis.set_major_formatter(FixedFormatter(["2,000", "5,000", "10,000", "20,000", "50,000"]))
a.set_title("Sumatra + Kalimantan fires vs Singapore PM2.5, 1 Aug–10 Oct", loc="left", color=INK, fontsize=12)
a.set_xlabel("MODIS fire detections (log scale)")
a.set_ylabel("Mean 24-h PM2.5, µg/m³ (NEA)")

for a in axes:
    a.grid(True, color=GRID, linewidth=0.8, zorder=0)
    for s in ["top", "right"]:
        a.spines[s].set_visible(False)
fig.text(0.01, 0.005, "MODIS standard product 2001–2025; 2026 (orange) is near-real-time, not directly comparable.",
         fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(f"{RES}/fires_r4.png", dpi=170)
print("saved")
