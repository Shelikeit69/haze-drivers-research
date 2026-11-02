# docs index

v2 first, v1 second, literature review last. Each entry links to the file and gives a one-line description drawn from the file itself.

## v2 (November 2026)

| File | What it is |
|---|---|
| [2026-11-02_v2_conclusions.md](2026-11-02_v2_conclusions.md) | **Start here.** Short, self-contained conclusions note for Plan v2: Step 0 replication of Sloan et al.'s fire events, Q1 and Q2 trend analyses, Q3 re-run of the v1 rain-fire link with Sloan's two suggestions, plus three figures and the Limits section. |
| [research_plan_v2.md](research_plan_v2.md) | Frozen research plan for v2. Pre-registration-style document written before T1–T6 confirmatory testing, with an honesty statement explaining which exploratory analyses were already seen and which were not. |
| [2026-11-02_v2_step0_validation.md](2026-11-02_v2_step0_validation.md) | Step 0 validation note: builds Sloan-style fire events from our FIRMS detections and compares them against Sloan's published Dryad events (2002–2019). Includes the Pearson r values, total counts, and the two construction differences (Collection 6.1 vs 6, Dec→Jan events). |
| [2026-11-02_v2_results.md](2026-11-02_v2_results.md) | Full results write-up for v2 Step 1 (Sloan trend replication), T1–T2 confirmatory WLS regressions, Holm correction across T1–T6, robustness checks (post-2016 step, block bootstrap, leave-one-out, Aqua-only), and exploratory analyses (skewness, 2019 vs 2023, LOWESS fire-energy vs rain). |
| [2026-11-02_v2_q3_results.md](2026-11-02_v2_q3_results.md) | Q3 results: re-runs of the v1 rain-fire link with Sloan's two suggestions — fire measured by FRP sum, and rain cumulative from June. Includes the FRP-vs-rain factor tables and the FRP-PM2.5 Spearman correlations for the Singapore link. |
| [v2_handoff.md](v2_handoff.md) | Working note for the v2 analysis. Records how the analysis was split across multiple scripts, how the Sloan Dryad CSV paths and FIRMS edge-month windows were settled, and what each v2 script writes to `results/`. Not a published result and not frozen. |

## v1 (October 2026)

| File | What it is |
|---|---|
| [paper_climate_fire_singapore_haze_2026-10-16.pdf](paper_climate_fire_singapore_haze_2026-10-16.pdf) | Short paper, 13 pages, 6 figures. The v1 write-up covering El Niño → Indonesian rain → fire → Singapore PM2.5, with the five planned tests. Revised 19 Oct 2026. |
| [research_plan_v1.md](research_plan_v1.md) | Frozen research plan for v1. Lists the five pre-registered tests (El Niño–Kalimantan rain, IOD–Sumatra rain, rain–fire detections, fires since 2016, fire–Singapore PM2.5) and the Holm-correction step. |
| [2026-10-16_confirmatory_results.md](2026-10-16_confirmatory_results.md) | Confirmatory results under v1: tables of the five planned tests with p-values before and after Holm correction, robustness checks, and post-2015 break-year range. |
| [2026-10-17_posthoc_reviewer_checks.md](2026-10-17_posthoc_reviewer_checks.md) | Post-hoc checks after reviewer feedback (17 and 19 Oct 2026). Negative-binomial re-specification, first differences, stationarity tests, and the break-year sensitivity range for the 77%/47% post-2016 fire-drop numbers. Outside the frozen v1 plan. |
| [2026-10-16_round4_fires.md](2026-10-16_round4_fires.md) | Round 4 analysis: drought, fires, and Singapore PM2.5. Introduces FIRMS fire detections, the Aug–Oct window, and the Singapore PM2.5 time series. The basis for the rain-fire and fire-haze links. |
| [2026-10-16_round3_gpcp.md](2026-10-16_round3_gpcp.md) | Round 3 analysis: re-tests the rain links with independent GPCP v2.3 monthly precipitation instead of ERA5. Verifies that v1's results are not driven by the SOI and ERA5 sharing a source. |
| [2026-10-16_round2_oni_iod.md](2026-10-16_round2_oni_iod.md) | Round 2 analysis: cross-checks the SOI against the official NOAA ONI, adds the Indian Ocean Dipole (DMI) as a second large-scale climate driver, and shows that DMI is the stronger predictor for Sumatra. |
| [2026-10-16_enso_correlation.md](2026-10-16_enso_correlation.md) | Round 1 analysis: the first pass. Builds a local SOI from ERA5 pressure, computes seasonal rain means on Sumatra and Kalimantan, and shows the El Niño–Kalimantan rain correlation that launched the rest of the project. |

## Literature review

| File | What it is |
|---|---|
| [literature_review.md](literature_review.md) | Literature review (v1, 16 Oct 2026). Covers the El Niño–Indonesian fire link, dry IOD events and Sumatra's 2015 and 2023 hazes, Sloan et al. 2022's event-based severity, and the open questions that v2 was designed to answer. |
