# Research plan v2 — DRAFT (not frozen)

Status: draft written 2 Nov 2026 for Toni's review. It becomes binding only when Toni approves it and the status line is changed to FROZEN with the date. After that, changes go in the dated "Deviations" section at the end.

Plan v1 (`docs/research_plan_v1.md`), its results and paper section 4.5 stay unchanged. v2 results are reported separately.

## Why v2

Dr Sean Sloan (Vancouver Island University) replied on 28 Oct 2026 with two suggestions:

1. Use the sum of fire radiative power (FRP) instead of detection counts.
2. Rain acts non-linearly and over two to three months, so use cumulative rain starting one to two months before the fire period.

His own published work (Sloan et al. 2022, Communications Earth & Environment 3:207, doi 10.1038/s43247-022-00522-6) measures fire severity at the level of fire events, controls for fire-season rain, and models the decline over time as a linear trend. v1 counted detections and used a 2016 step. v2 does three things: replicates his event method on our data, extends it past 2019, and re-runs our v1 fire model with his two suggestions.

## Honesty statement (will appear in the write-up)

This is not a pre-registration. Before writing it we had already seen:

- Aug–Oct MODIS detection counts for 2001–2026 and the fitted rain–fire models of v1, including the post-hoc break-year scan.
- Yearly Aug–Oct FRP totals: `frp_sum_mw` is in `results/fire_counts_r4.csv`. No model was fitted to them, but the numbers sit in a file we produced.
- Sloan et al.'s published estimates for 2002–2019.

We have not seen: MODIS detections for June–July and November–January, any event-level data (ours or Sloan's Dryad files), or CHIRPS rain. The plan fixes the analysis before those are downloaded.

## Questions

- Q1 (replication). Using Sloan's event definitions on 2002–2019, do we reproduce his events and his direction and size of decline in severe fire events, for Sumatra and Kalimantan?
- Q2 (extension). Does the decline, controlling for fire-season rain, still hold over 2002–2025, which adds the 2023 El Niño season?
- Q3 (v1 model, Sloan's suggestions). Does the v1 rain–fire link hold when fires are measured by FRP sum, and when rain is cumulative from before the season?

## Fixed data and definitions

| Item | Choice |
|---|---|
| Fire data | NASA FIRMS MODIS standard product (MODIS_SP, Collection 6.1, Terra + Aqua), same download box as v1 (lon 100–116.5, lat −5 to 2.3) |
| Download window | 1 Jun – 31 Jan of the next year, 2002–2025, so events near the season edges are not cut off |
| Regions | v1 island boxes in `src/analyse_r4.py` (Sumatra incl. Bangka; Kalimantan excl. most of Sarawak). Sloan's province-based regions are not rebuilt; differences are stated, not adjusted |
| Fire event | Detections in the same or an adjacent (8-neighbour) cell of a 1 km equal-area grid, within 4 days of a detection already in the event. Ignition date = earliest detection date |
| Season assignment | An event belongs to the Jul–Dec season of its ignition date. Events igniting outside Jul–Dec are dropped |
| Event severity | Sum of FRP (MW) over the event × duration in days (minimum 1) |
| Severe / very severe | Sloan's published national thresholds: severity ≥ 60.4 (severe), ≥ 216 (very severe). Not re-derived from our regions |
| Rain, primary | CHIRPS v2.0 monthly (0.05°), mean over land cells inside each island box |
| Rain, sensitivity | GPCP v2.3 (already in `data/raw`, v1 cells); IMERG V07 only if Toni downloads it (needs an Earthdata login) |
| Years | Replication 2002–2019 (18 seasons); extension 2002–2025 (24 seasons). 2026 excluded: no standard product yet and the season is incomplete |

## Step 0 — validate the event construction against Sloan's data

Sloan's event table is on Dryad (doi 10.5061/dryad.msbcc2g1t). Its exact fields are checked at download and recorded here as a deviation if they differ from what this plan assumes.

1. Restrict the Dryad events to our two island boxes and to Jul–Dec ignitions, 2002–2019.
2. Build our events from the FIRMS detections with the definitions above.
3. Compare, by year and island: number of events, number of severe and very severe events, and median severity.

Pass rule, fixed now: for both islands, the yearly count of severe events has Pearson r ≥ 0.95 with Dryad, and the 18-season totals of events and of severe events are each within ±10% of Dryad.

If it fails: first switch to 4-neighbour adjacency and to type-0 detections only (both are plausible readings of the paper's definitions), one at a time, and re-check. These choices are made on event-level agreement with Dryad, before any trend or rain model is fitted. If none passes, report the mismatch, use the Dryad events for Q1, and flag the 2020–2025 extension as built with an unvalidated event method.

Known source of mismatch: Sloan used MCD14ML Collection 6; FIRMS serves Collection 6.1.

## Step 1 — replication (Q1), 2002–2019

Outcome models, per island, as in Sloan et al.:

- (a) Annual proportion of Jul–Dec events that are severe, and very severe: proportion ~ Jul–Dec rain + linear year (year − 2002). Weighted by the number of detections that year.
- (b) Seasonal severity: skewness of the event-severity distribution in each Jul–Dec season ~ Jul–Dec rain + linear year.

Uncertainty: 1,000 bootstrap resamples of years (Sloan's setting); robustness by dropping 2015 and by dropping 2019, as he did.

Reporting: the year coefficient converted to a % change over 2002–2019, next to Sloan's regional figures. No p-values here; the question is whether we reproduce his direction and size. Our regions differ from his, so a match "in direction and roughly in size" is the expected best case.

## Step 2 — confirmatory tests (Q2 and Q3), Holm-corrected together, α = 0.05

| # | Test | Model | Years |
|---|---|---|---|
| T1 | Severe-event share falls over time, Sumatra | year coefficient < 0 in model (a), severe | 2002–2025 |
| T2 | Same, Kalimantan | as T1 | 2002–2025 |
| T3 | Less rain → more fire energy, Sumatra | rain coefficient in log10(Aug–Oct FRP sum) ~ Aug–Oct rain + post2016 | 2002–2025 |
| T4 | Same, Kalimantan | as T3 | 2002–2025 |
| T5 | Cumulative rain version, Sumatra | rain coefficient in log10(Aug–Oct FRP sum) ~ cumulative Jun–Oct rain + post2016 | 2002–2025 |
| T6 | Same, Kalimantan | as T5 | 2002–2025 |

Notes on the choices:

- T3–T6 keep v1's Aug–Oct fire window and 2016 step so the only change from v1 H3 is the one Sloan suggested. They use CHIRPS, not GPCP, so a GPCP run of T3–T6 is reported next to them to separate the effect of the rain product.
- Years for T3–T6 start at 2002 (not v1's 2001) so all v2 tests share one sample.
- "Cumulative from two months before" means Jun–Oct for an Aug–Oct fire window. This is the primary form; one month before (Jul–Oct) is the secondary form.
- Rain enters linearly in the primary models, as in Sloan et al.

## Robustness (all reported, none used to choose results)

1. Rain form: log(rain), and the cumulative-rain window starting one month before (Jul–Oct).
2. Time form: linear trend instead of the 2016 step in T3–T6, and the 2016 step instead of the linear trend in T1–T2.
3. Dependence between years: moving-block bootstrap, blocks of 3 years, 10,000 resamples.
4. Leave-one-year-out range for T1–T6.
5. Satellite drift: Terra's and Aqua's overpass times have drifted in recent years (source to be cited in the write-up). Re-run T1–T6 with Aqua detections only.
6. VIIRS (S-NPP, 2012 onward): yearly Aug–Oct FRP sum per island as a check on the MODIS FRP trend. Not used for events (375 m pixels do not fit a 1 km event grid).
7. Singapore link: v1 H4 (Spearman, 2016–2025) re-run with FRP sum instead of counts. Reported as a robustness check on H4, not a new test.

## Exploratory (no significance claims)

- Model (b) skewness over 2002–2025.
- 2019 vs 2023: both El Niño-type dry seasons; compare event counts, severity distribution and rain.
- Whether the rain–fire link looks like a threshold (scatter with a smoother), in light of Sloan's point that rain acts non-linearly.

## Not in v2

National Indonesia replication (needs a much larger download and province boundaries). The Jan–Jun season. Modelling Singapore PM2.5 directly or as excess over a non-haze baseline (still open from the Reddit review). Palm-oil economics.

## Data to download before running

| Data | Who | Notes |
|---|---|---|
| FIRMS MODIS_SP, 1 Jun – 31 Jan, 2002–2025, same box | Claude, with Toni's FIRMS key in the session environment; Toni locally if the workspace cannot reach FIRMS | Extends `src/fetch_firms.py`; existing Aug–Oct files reused |
| Sloan et al. event data, Dryad | Toni (Dryad likely not reachable from the workspace) | Save unchanged under `data/raw/sloan_dryad/` |
| CHIRPS v2.0 monthly, 2002–2025 | Toni (data.chc.ucsb.edu) | Clip to lon 100–116.5, lat −5 to 2.3 to keep the file small |
| VIIRS S-NPP (FIRMS VIIRS_SNPP_SP), Aug–Oct 2012–2025 | Same route as MODIS | Robustness 6 only |

All raw files are added to `data/raw/SHA256SUMS.txt`.

## Order of work

1. Toni approves this plan; it is frozen and committed before any new data is opened.
2. Download the data above.
3. Step 0 (validation), then Step 1, then Step 2 and the robustness checks.
4. Write a short v2 note (`docs/<date>_v2_results.md`); decide afterwards whether it becomes a new paper section.
5. Reply to Sloan with the v2 results, and correct two points from the 16 Oct email: the paper is 13 pages, and the 77% / 47% drops belong to a 2016 break and change with the break year.

## Deviations

(none yet)
