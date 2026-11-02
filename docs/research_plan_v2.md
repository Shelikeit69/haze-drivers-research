# Research plan v2 — FROZEN

Status: approved by Toni and frozen on 2 Nov 2026. A first draft was committed earlier the same day (72756d5). This version is binding. Any later change goes in the dated "Deviations" section at the end.

Plan v1 (`docs/research_plan_v1.md`), its results and paper section 4.5 stay unchanged. v2 results are reported separately.

## Why v2

Dr Sean Sloan (Vancouver Island University) replied on 28 Oct 2026 with two suggestions:

1. Use the sum of fire radiative power (FRP) instead of detection counts.
2. Rain acts non-linearly and over two to three months, so use cumulative rain starting one to two months before the fire period.

His own published work (Sloan et al. 2022, Communications Earth & Environment 3:207, doi 10.1038/s43247-022-00522-6) measures fire severity at the level of fire events, controls for fire-season rain, and models the decline over time as a linear trend. v1 counted detections and used a 2016 step. v2 does three things: it replicates his event method on our data, extends it past 2019, and re-runs our v1 fire model with his two suggestions.

## Honesty statement (will appear in the write-up)

This is not a pre-registration. Before writing it we had already seen:

- Aug–Oct MODIS detection counts for 2001–2026 and the fitted rain–fire models of v1, including the post-hoc break-year scan.
- Yearly Aug–Oct FRP totals: `frp_sum_mw` is in `results/fire_counts_r4.csv`. No model was fitted to them, but the numbers sit in a file we produced.
- GPCP monthly rain for all months, since the whole GPCP file has been in `data/raw` since round 3. Only Aug–Oct means were used in v1.
- Sloan et al.'s published estimates for 2002–2019.

We have not seen: MODIS detections for June–July and November–January, the contents of Sloan's Dryad event tables (received 2 Nov 2026, only file names and sizes checked before this plan was frozen), or CHIRPS rain. The plan fixes the analysis before those are opened.

## Questions

- Q1 (replication). Using Sloan's event definitions on 2002–2019, do we reproduce his events and his direction and size of decline in severe fire events, for Sumatra and Kalimantan?
- Q2 (extension). Does the decline, controlling for fire-season rain, still hold over 2002–2025, which adds the 2023 El Niño season?
- Q3 (v1 model, Sloan's suggestions). Does the v1 rain–fire link hold when fires are measured by FRP sum, and when rain is cumulative from before the season?

## Fixed data and definitions

| Item | Choice |
|---|---|
| Fire data | NASA FIRMS MODIS standard product (MODIS_SP, Collection 6.1, Terra and Aqua), same download box as v1 (lon 100–116.5, lat −5 to 2.3) |
| Download window | 1 Jun – 31 Jan of the next year, 2002–2025, so events near the season edges are not cut off |
| Regions | v1 island boxes in `src/analyse_r4.py` (Sumatra including Bangka; Kalimantan without most of Sarawak). Sloan's province-based regions are not rebuilt; differences are stated, not adjusted |
| Fire event | Detections in the same or an adjacent (8-neighbour) cell of a 1 km equal-area grid, within 4 days of a detection already in the event. Ignition date = earliest detection date |
| Season assignment | An event belongs to the Jul–Dec season of its ignition date. Events igniting outside Jul–Dec are dropped |
| Event severity | Sum of FRP (MW) over the event × (duration in days + 1), the same as `FRP_Days` in Sloan's Dryad tables |
| Severe / very severe | Sloan's published national thresholds: severity ≥ 60.4 (severe), ≥ 216 (very severe). Not re-derived from our regions |
| Rain, primary | GPCP v2.3 monthly, mean of the three v1 cells per island (`results/gpcp_cells_r3.csv`). Same product and cells as v1, so the only change from v1 in Q3 is the one Sloan suggested |
| Rain units | Aug–Oct: mean mm/day (v1 units). Cumulative windows (Jun–Oct, Jul–Oct, Jul–Dec): total mm, summing monthly mm/day × days in month |
| Rain, sensitivity | CHIRPS v2.0 monthly, if a working download is found; IMERG V07 only if Toni downloads it (needs an Earthdata login) |
| Years | Replication 2002–2019 (18 seasons); extension 2002–2025 (24 seasons). 2026 excluded: no standard product yet and the season is incomplete |

## Step 0: validate the event construction against Sloan's data

Sloan's event tables come from Dryad (doi 10.5061/dryad.msbcc2g1t, version of 28 Aug 2022). The detection table (`nfire4_all_spatial_fire_2002_2019_joins_sp_LC.csv`) carries the event fields for every detection, with coordinates (`POINT_X`, `POINT_Y`), an island code and `FRP_Days`.

1. Restrict the Dryad detections to our two island boxes by their coordinates, and keep events whose ignition falls in Jul–Dec, 2002–2019. The Dryad island code is reported as a cross-check only.
2. Build our events from the FIRMS detections with the definitions above.
3. Compare, by year and island: number of events, number of severe and very severe events, and median severity.

Pass rule: for both islands, the yearly count of severe events has Pearson r ≥ 0.95 with Dryad, and the 18-season totals of events and of severe events are each within ±10% of Dryad.

If it fails: first switch to 4-neighbour adjacency, then to type-0 detections only (both are plausible readings of the paper's definitions), one at a time, and check again. These choices are made on event-level agreement with Dryad, before any trend or rain model is fitted. If none passes, report the mismatch, use the Dryad events for Q1, and flag the 2020–2025 extension as built with an unvalidated event method.

Known source of mismatch: Sloan used MCD14ML Collection 6; FIRMS serves Collection 6.1.

## Step 1: replication (Q1), 2002–2019

Outcome models, per island, as in Sloan et al.:

- (a) Annual proportion of Jul–Dec events that are severe, and very severe: proportion ~ Jul–Dec rain + linear year (year − 2002). Weighted by the number of detections that year.
- (b) Seasonal severity: skewness of the event-severity distribution in each Jul–Dec season ~ Jul–Dec rain + linear year.

Uncertainty: 1,000 bootstrap resamples of years (Sloan's setting); robustness by dropping 2015 and by dropping 2019, as he did.

Reporting: the year coefficient converted to a % change over 2002–2019, next to Sloan's regional figures. No p-values here; the question is whether we reproduce his direction and size. Our regions differ from his, so a match in direction and roughly in size is the expected best case.

## Step 2: confirmatory tests (Q2 and Q3), Holm-corrected together, α = 0.05

| # | Test | Model | Years |
|---|---|---|---|
| T1 | Severe-event share falls over time, Sumatra | year coefficient < 0 in model (a), severe | 2002–2025 |
| T2 | Same, Kalimantan | as T1 | 2002–2025 |
| T3 | Less rain → more fire energy, Sumatra | rain coefficient in log10(Aug–Oct FRP sum) ~ Aug–Oct rain + post2016 | 2002–2025 |
| T4 | Same, Kalimantan | as T3 | 2002–2025 |
| T5 | Cumulative rain version, Sumatra | rain coefficient in log10(Aug–Oct FRP sum) ~ cumulative Jun–Oct rain + post2016 | 2002–2025 |
| T6 | Same, Kalimantan | as T5 | 2002–2025 |

Notes on the choices:

- T3–T6 keep v1's Aug–Oct fire window, GPCP cells and 2016 step, so the only change from v1 H3 is the one Sloan suggested.
- Years start at 2002 (not v1's 2001) so all v2 tests share one sample.
- "Cumulative from two months before" means Jun–Oct for an Aug–Oct fire window. This is the primary form; one month before (Jul–Oct) is the secondary form.
- Rain enters linearly in the primary models, as in Sloan et al.
- T3–T6 need no new data and run first. Their unadjusted p-values are reported when they run; the Holm adjustment over all six tests is applied once T1–T2 are available.
- p-values come from ordinary least squares (T3–T6) and weighted least squares (T1–T2); 95% intervals from 10,000 bootstrap resamples of years.

## Robustness (all reported, none used to choose results)

1. Rain form: log(rain), and the cumulative window starting one month before (Jul–Oct).
2. Time form: linear trend instead of the 2016 step in T3–T6, and the 2016 step instead of the linear trend in T1–T2.
3. Dependence between years: moving-block bootstrap, blocks of 3 years, 10,000 resamples.
4. Leave-one-year-out range for T1–T6.
5. Satellite drift: the overpass times of Terra and Aqua have drifted in recent years (source to be cited in the write-up). Re-run T1–T6 with Aqua detections only.
6. VIIRS (S-NPP, 2012 onward): yearly Aug–Oct FRP sum per island as a check on the MODIS FRP trend. Not used for events (375 m pixels do not fit a 1 km event grid).
7. Singapore link: v1 H4 (Spearman, 2016–2025) re-run with FRP sum instead of counts. Reported as a robustness check on H4, not a new test.
8. Rain product: T1–T6 with CHIRPS instead of GPCP, if CHIRPS is obtained.

## Exploratory (no significance claims)

- Model (b) skewness over 2002–2025.
- 2019 against 2023: both dry El Niño-type seasons; compare event counts, severity distribution and rain.
- Whether the rain–fire link looks like a threshold (scatter with a smoother), in light of Sloan's point that rain acts non-linearly.

## Not in v2

National Indonesia replication (needs a much larger download and province boundaries). The Jan–Jun season. Modelling Singapore PM2.5 directly or as excess over a non-haze baseline (still open from the Reddit review). Palm-oil economics.

## Data

| Data | Status |
|---|---|
| GPCP v2.3 monthly | In `data/raw` since round 3 |
| FIRMS MODIS_SP Aug–Oct, 2002–2025 | In `data/raw/firms` (v1) |
| FIRMS MODIS_SP, 1 Jun – 31 Jan, 2002–2025, same box | To download. The workspace reaches FIRMS; needs Toni's key in the session environment. Extends `src/fetch_firms.py`; existing files reused |
| Sloan et al. event data, Dryad | Received 2 Nov 2026, `doi_10_5061_dryad_msbcc2g1t__v20220828.zip`, SHA256 `0b76226376a13cc8212df0f07041597cd169fba9c7cbdcd8cb6541e80a789e3b`. At 202 MB it is above GitHub's file limit, so it is not committed; anyone can download it from Dryad and check the hash |
| CHIRPS v2.0 monthly | Optional (robustness 8); download route still to be found |
| VIIRS S-NPP (FIRMS VIIRS_SNPP_SP), Aug–Oct 2012–2025 | To download, same route as MODIS (robustness 6) |

All committed raw files are listed in `data/raw/SHA256SUMS.txt`.

## Order of work

1. Plan frozen and committed before any new data is opened.
2. Q3: T3–T6 and their robustness checks, from data already in the repo.
3. Step 0 (validation against Dryad), then Step 1, then T1–T2 and the Holm adjustment.
4. Write a short v2 note (`docs/<date>_v2_results.md`); decide afterwards whether it becomes a new paper section.
5. Reply to Sloan with the v2 results, and correct two points from the 16 Oct email: the paper is 13 pages, and the 77% and 47% drops belong to a 2016 break and change with the break year.

## Deviations

### 2 Nov 2026 — clarification before Step 1, fixed by reviewer before any Step 1 or T1-T2 result was seen

1. **T1 and T2 report two-sided p-values**, consistent with T3 to T6, together with the sign of the year coefficient.
2. **WLS weights for model (a)** are the number of fire points (detections) in all retained events — that is, events igniting in Jul–Dec — that fall inside the island box, for that island and year.
3. **Seasonal severity skewness** is `scipy.stats.skew(severity, bias=False)`, computed per island and per year over the events igniting in Jul–Dec of that year.
4. **Step 1 "% change over 2002–2019"** is `100 × 17 × b ÷ fitted value in 2002 at the sample-mean rain`, where `b` is the year coefficient. For skewness the same formula is applied by analogy. The bootstrap 95 percent interval uses the same formula in each resample.
5. **All events are built by `src/v2_step0.py:build_events`** with the validated configuration (8-neighbour, all detections). No separate event builder is written. The same function and the same raw data (`data/raw/firms` plus `data/raw/firms_v2`) are used for 2020–2025; `build_events` and `load_firms` were given optional `years`/`start`/`end` parameters with defaults that leave the Step 0 output byte-identical.
