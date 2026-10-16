"""Two scatter panels: SOI vs Kalimantan dry-season rain (1950-2025) and
SOI vs Singapore PM2.5, 1 Aug-10 Oct (2016-2026)."""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RES = sys.argv[1] if len(sys.argv) > 1 else "results"
y = pd.read_csv(f"{RES}/yearly.csv", index_col=0)

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#1f1f1e", "#6b6a63", "#e6e5df"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED})

fig, axes = plt.subplots(2, 1, figsize=(6.4, 9.6))

# Panel 1
a = axes[0]
d = y.loc[1950:2025, ["soi_aso", "rain_kalimantan_aso"]].dropna()
a.scatter(d["soi_aso"], d["rain_kalimantan_aso"], s=46, color=BLUE, edgecolor="white", linewidth=1.2, zorder=3)
OFF1 = {1982: (6, 4), 1997: (6, 4), 2006: (6, -12), 2015: (-10, -16)}
for yr, off in OFF1.items():
    a.annotate(str(yr), (d.loc[yr, "soi_aso"], d.loc[yr, "rain_kalimantan_aso"]),
               xytext=off, textcoords="offset points", color=INK, fontsize=10)
a.axhline(4, color=MUTED, linewidth=1, linestyle="--", zorder=1)
a.text(d["soi_aso"].max(), 4.25, "4 mm/day", ha="right", color=MUTED, fontsize=9)
a.set_title("El Niño and Kalimantan Aug–Oct rain, 1950–2025 (n=76)", loc="left", color=INK, fontsize=12)
a.set_xlabel("SOI, Aug–Oct (negative = El Niño)")
a.set_ylabel("Rain, mm/day (ERA5)")

# Panel 2
a = axes[1]
d = y.loc[2016:2026, ["soi_jja", "w_sg_pm25_mean"]].dropna()
base = d.drop(index=2026)
a.scatter(base["soi_jja"], base["w_sg_pm25_mean"], s=56, color=BLUE, edgecolor="white", linewidth=1.2, zorder=3)
a.scatter([d.loc[2026, "soi_jja"]], [d.loc[2026, "w_sg_pm25_mean"]], s=70, color=ORANGE,
          edgecolor="white", linewidth=1.2, zorder=4)
for yr in d.index:
    a.annotate(str(yr), (d.loc[yr, "soi_jja"], d.loc[yr, "w_sg_pm25_mean"]),
               xytext={2024: (-8, -14), 2017: (6, 2)}.get(yr, (6, 4)), textcoords="offset points", color=INK, fontsize=9)
a.set_title("June–Aug SOI vs Singapore PM2.5, 1 Aug–10 Oct", loc="left", color=INK, fontsize=12)
a.set_xlabel("SOI, Jun–Aug (negative = El Niño)")
a.set_ylabel("Mean 24-h PM2.5, µg/m³ (NEA, 5 regions)")

for a in axes:
    a.grid(True, color=GRID, linewidth=0.8, zorder=0)
    for s in ["top", "right"]:
        a.spines[s].set_visible(False)

fig.text(0.01, 0.005, "SOI computed from ERA5 Tahiti–Darwin pressure (1981–2010 base). 2026 in orange; 2019 has 13 days missing.",
         fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(f"{RES}/enso_haze.png", dpi=170)
print("saved")
