"""Figures for the v2 documentation update.

This script reads only files that are already in ``results/``. It does not
re-run any analysis model or rebuild any event. The two trend/scatter images
used in the conclusions report (``v2_t1t2_trend.png`` and
``v2_exploratory_frp_rain.png``) were produced by ``src/v2_stage2.py`` and are
reused here; this script draws only the Step 0 replication figure.

Usage:
    python src/v2_figures.py results
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


def _build_step0_replication(results_dir: str) -> str:
    yearly = pd.read_csv(os.path.join(results_dir, "v2_step0_yearly.csv"))
    comp = pd.read_csv(os.path.join(results_dir, "v2_step0_comparison.csv"))

    ours_scenario = "8-neighbour, all detections"

    out = os.path.join(results_dir, "v2_fig_step0_replication.png")

    islands = [("sumatra", "Sumatra"), ("kalimantan", "Kalimantan")]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=False, dpi=150)

    r_lookup = dict(zip(comp["island"], comp["r_severe"]))

    for ax, (island_key, island_label) in zip(axes, islands):
        ours = yearly[
            (yearly["scenario"] == ours_scenario)
            & (yearly["source"] == "ours")
            & (yearly["island"] == island_key)
        ].sort_values("year")
        dryad = yearly[
            (yearly["scenario"] == "dryad")
            & (yearly["source"] == "dryad")
            & (yearly["island"] == island_key)
        ].sort_values("year")

        ax.plot(
            ours["year"], ours["n_severe"],
            marker="o", linewidth=1.6, markersize=4,
            color="#1f77b4", label="ours",
        )
        ax.plot(
            dryad["year"], dryad["n_severe"],
            marker="s", linewidth=1.2, markersize=3.5, linestyle="--",
            color="#d62728", label="Sloan Dryad",
        )
        r = r_lookup[island_key]
        ax.set_title(f"{island_label}  (r = {r:.5f})", fontsize=10.5)
        ax.set_xlabel("Year")
        ax.set_ylabel("Severe events per year")
        ax.set_xlim(2002, 2019)
        ax.set_xticks(range(2002, 2020, 2))
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.legend(loc="best", fontsize=9)

    fig.suptitle(
        "Severe fire events: our event construction versus Sloan et al. (Dryad), 2002\u20132019",
        fontsize=11,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    if len(sys.argv) > 1:
        results_dir = sys.argv[1]
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        results_dir = os.path.normpath(os.path.join(here, "..", "results"))

    step0_fig = _build_step0_replication(results_dir)
    print(f"wrote {step0_fig}")

    reused = ["v2_t1t2_trend.png", "v2_exploratory_frp_rain.png"]
    for name in reused:
        path = os.path.join(results_dir, name)
        if not os.path.isfile(path):
            print(f"warning: expected figure missing: {path}", file=sys.stderr)
        else:
            print(f"reusing {path}")


if __name__ == "__main__":
    main()
