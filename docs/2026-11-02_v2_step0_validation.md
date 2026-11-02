# Step 0 validation: FIRMS events against Sloan et al. (Dryad)

Date: 2 November 2026
Branch: `v2-step0`
Script: `src/v2_step0.py`
Results: `results/v2_step0_yearly.csv`, `results/v2_step0_comparison.csv`,
`results/v2_step0_crosscheck.csv`, `results/v2_step0_empty_firms_v2.csv`

This note covers Step 0 only. No trend model, rainfall model, or Step 1 work was run.

## 1. Data and definitions

FIRMS detections are `MODIS_SP` only, from `data/raw/firms/` and `data/raw/firms_v2/`.
The validation window is 1 June 2002 to 31 January 2020, which covers the 2002-2019
Jul-Dec seasons plus the edge detections needed for events that ignite in December and
continue into January. In this window the script loads 912,280 detections; 42,555
detections fall outside the two island boxes and are dropped, leaving 869,725 detections.

Event construction follows the frozen plan:

- grid: 1 km equal-area cells in the MODIS sinusoidal projection
  (`x = R cos(lat) lon`, `y = R lat`, cells by integer floor of kilometres);
- adjacency: 8-neighbour cells (same cell or any of the eight surrounding cells);
- time: a detection is linked when its date is within four days of a detection already
  in the event; events are connected components of these links;
- ignition date: earliest detection date in the event;
- season: the event belongs to the Jul-Dec season of its ignition year; events igniting
  outside Jul-Dec, or outside 2002-2019, are dropped;
- severity: `sum(FRP) * (duration in days + 1)`, with duration equal to the difference
  between the last and first detection dates;
- severe event: severity >= 60.4; very severe event: severity >= 216.

The Dryad README defines AFD as active fire detection. Sloan's events are AFDs in the
same or an adjacent 1 km2 grid cell within four days, built per island and per calendar
year. `MIN_acq_yer` and `MIN_acq_mnt` give ignition, `RANGE_yday` is the last minus first
detection day, `AF_Count` is the number of AFDs, and `FRP_Days` is `SUM_FRP * (RANGE_yday
+ 1)`. Island code 1000000 is Sumatra and 2000000 is Kalimantan. Our construction follows
the plan and allows an event to continue from December into January; Sloan does not allow
an event to cross a calendar year. This difference affects only events at the year
boundary.

On the Dryad side, detections are restricted to the v1 island boxes with the `island`
function from `src/analyse_r4.py`. An event is kept when at least one detection falls in a
box, is assigned to the box holding most of its detections, and is kept when its ignition
is Jul-Dec 2002-2019. Event attributes are Sloan's full-event values; the box restriction
does not recompute `FRP_Days`. The Dryad `Island` code is used only as a cross-check.

## 2. Dryad data verification

The full dataset zip `doi_10_5061_dryad_msbcc2g1t__v20220828.zip` was assembled from the
two Dryad file streams with the same client-side zip procedure that the Dryad download
button uses (file names, order, and S3 `Last-Modified` timestamps). Its SHA256 is
`0b76226376a13cc8212df0f07041597cd169fba9c7cbdcd8cb6541e80a789e3b`, which matches the
value in the frozen plan. The check is recorded in `results/v2_step0_crosscheck.csv`
(`dryad_zip_sha256_matches_plan = True`). The archive was extracted to
`data/external/sloan_dryad/`, which is ignored by git.

Dryad rows inside the boxes: 953,455 detections and 344,263 events before the Jul-Dec and
year filters. Of these, 290,592 events are kept for 2002-2019 Jul-Dec. Ten detections and
nine kept events have a missing or non-island Dryad `Island` code. Among detections and
events that do have a code, the code agrees with the coordinate-based box in every case
(0 mismatches). All cross-check numbers are in `results/v2_step0_crosscheck.csv`.

## 3. Primary result

The primary configuration is 8-neighbour adjacency with all detection types. It passes
every element of the plan's criterion for both islands:

| Island | Severe r (18 years) | Events ours | Events Dryad | Ratio | Severe ours | Severe Dryad | Ratio | Pass |
|---|---|---|---|---|---|---|---|---|
| Sumatra | 0.999545 | 123,046 | 121,306 | 1.014344 | 32,588 | 32,498 | 1.002769 | True |
| Kalimantan | 0.999976 | 171,631 | 169,286 | 1.013852 | 54,264 | 53,838 | 1.007913 | True |

The full comparison file also reports `r_events` (0.999969 for Sumatra, 0.999990 for
Kalimantan) and `r_very_severe` (0.999326 and 0.999921). Both event totals are within
1.5 percent of Dryad and both severe totals are within 1 percent, so the +/-10 percent
totals condition holds for both islands. The severe-event Pearson r condition (>= 0.95)
holds for both islands. `pass_scenario = True`.

Median severity also agrees closely. The overall median is 23.2 for Sumatra in our events
and 23.5 in Dryad, and 28.5 for Kalimantan in our events and 28.8 in Dryad. The largest
absolute difference between our and Dryad yearly medians is 2.0 for Sumatra and 0.7 for
Kalimantan (`results/v2_step0_comparison.csv`).

## 4. Yearly comparison, primary configuration

All values below are from `results/v2_step0_yearly.csv`.

### Sumatra

| Year | Events (ours) | Events (Dryad) | Severe (ours) | Severe (Dryad) | Very severe (ours) | Very severe (Dryad) | Median severity (ours) | Median severity (Dryad) |
|---|---|---|---|---|---|---|---|---|
| 2002 | 9062 | 8983 | 2448 | 2562 | 984 | 1043 | 23.6 | 25.6 |
| 2003 | 5769 | 5726 | 1480 | 1473 | 539 | 535 | 24.1 | 24.1 |
| 2004 | 8834 | 8673 | 2434 | 2434 | 934 | 959 | 24.7 | 25.1 |
| 2005 | 6543 | 6480 | 1610 | 1603 | 597 | 584 | 23.1 | 23.1 |
| 2006 | 16110 | 15904 | 4728 | 4689 | 2087 | 2058 | 25.4 | 25.6 |
| 2007 | 6755 | 6673 | 1604 | 1587 | 560 | 550 | 21.6 | 21.8 |
| 2008 | 6107 | 6021 | 1700 | 1682 | 666 | 669 | 24.6 | 24.8 |
| 2009 | 9002 | 8868 | 2540 | 2542 | 1007 | 996 | 25.0 | 25.2 |
| 2010 | 3067 | 3013 | 543 | 549 | 169 | 164 | 19.5 | 19.4 |
| 2011 | 8291 | 8167 | 2203 | 2166 | 864 | 868 | 23.6 | 23.7 |
| 2012 | 8633 | 8485 | 2381 | 2350 | 970 | 952 | 23.8 | 24.1 |
| 2013 | 4611 | 4496 | 1285 | 1270 | 549 | 542 | 24.0 | 24.5 |
| 2014 | 7140 | 7050 | 1788 | 1813 | 755 | 747 | 21.9 | 22.2 |
| 2015 | 11634 | 11420 | 3334 | 3294 | 1643 | 1618 | 23.8 | 23.8 |
| 2016 | 1911 | 1891 | 334 | 330 | 110 | 109 | 17.5 | 17.1 |
| 2017 | 1557 | 1526 | 193 | 190 | 52 | 55 | 16.0 | 16.0 |
| 2018 | 2085 | 2082 | 340 | 344 | 123 | 117 | 16.4 | 16.6 |
| 2019 | 5935 | 5848 | 1643 | 1620 | 833 | 831 | 21.9 | 22.3 |
| **Total** | **123046** | **121306** | **32588** | **32498** | **13442** | **13397** | | |

### Kalimantan

| Year | Events (ours) | Events (Dryad) | Severe (ours) | Severe (Dryad) | Very severe (ours) | Very severe (Dryad) | Median severity (ours) | Median severity (Dryad) |
|---|---|---|---|---|---|---|---|---|
| 2002 | 17913 | 17609 | 6319 | 6281 | 3240 | 3259 | 30.7 | 31.4 |
| 2003 | 9734 | 9604 | 3222 | 3187 | 1255 | 1256 | 31.7 | 31.9 |
| 2004 | 14704 | 14519 | 5187 | 5159 | 2494 | 2502 | 32.0 | 32.7 |
| 2005 | 7641 | 7551 | 2205 | 2158 | 812 | 794 | 27.2 | 27.4 |
| 2006 | 20811 | 20501 | 7314 | 7263 | 3452 | 3474 | 31.3 | 31.8 |
| 2007 | 6003 | 5935 | 1544 | 1522 | 544 | 519 | 24.6 | 24.4 |
| 2008 | 4161 | 4107 | 1045 | 1038 | 290 | 289 | 24.2 | 24.2 |
| 2009 | 15200 | 14985 | 5202 | 5139 | 2452 | 2426 | 31.0 | 31.4 |
| 2010 | 1953 | 1930 | 309 | 299 | 54 | 49 | 19.8 | 20.0 |
| 2011 | 9129 | 9028 | 2547 | 2515 | 940 | 935 | 26.0 | 25.9 |
| 2012 | 9534 | 9405 | 2736 | 2712 | 1026 | 1024 | 27.1 | 27.1 |
| 2013 | 6341 | 6245 | 1782 | 1768 | 646 | 647 | 27.6 | 27.7 |
| 2014 | 12026 | 11925 | 3701 | 3700 | 1619 | 1633 | 27.9 | 28.2 |
| 2015 | 17706 | 17468 | 6085 | 6073 | 2928 | 2974 | 30.3 | 30.5 |
| 2016 | 2968 | 2929 | 650 | 630 | 167 | 159 | 23.5 | 23.6 |
| 2017 | 1983 | 1949 | 319 | 318 | 79 | 77 | 19.1 | 19.3 |
| 2018 | 5081 | 5021 | 1330 | 1333 | 502 | 504 | 25.0 | 25.5 |
| 2019 | 8743 | 8575 | 2767 | 2743 | 1309 | 1298 | 26.4 | 26.8 |
| **Total** | **171631** | **169286** | **54264** | **53838** | **23809** | **23819** | | |

## 5. Fallbacks

The plan specifies that the 4-neighbour and type-0 variants are tried only if the primary
configuration fails, in that order, with one change at a time. The primary configuration
passed, so neither fallback was run. `results/v2_step0_comparison.csv` therefore contains
one scenario only: `8-neighbour, all detections`. No other adjustment was applied.

## 6. Collection 6 and Collection 6.1

This project's FIRMS data are Collection 6.1 (`MODIS_SP`). Sloan et al. mapped fires with
MODIS Collection 6. The MODIS Collection 6 and 6.1 active fire products use the same
science algorithm; the Collection 6.1 changes are calibration improvements in the Level 1B
inputs, especially the response-versus-scan angle approach and corrections for infrared
crosstalk. NASA states that the two collections are sufficiently consistent to be
intermixed, with only slight differences in detected fire pixels. Those calibration
differences are the expected source of any small differences between our detections and
Sloan's, such as the roughly 1.4 percent higher event totals in our events. The validation
therefore tests whether the event construction reproduces Sloan's structure, not whether
the two collections are byte-identical.

Sources: the [MODIS Collection 6 and 6.1 Active Fire Product User's Guide](https://landweb.modaps.eosdis.nasa.gov/data/userguide/MODIS_C6_C6.1_Fire_User_Guide_1.0.pdf)
and the NASA Earthdata version descriptions for the MODIS 6.1 fire products.

## 7. Empty FIRMS v2 files

`results/v2_step0_empty_firms_v2.csv` lists nine `MODIS_SP` files in `data/raw/firms_v2/`
with zero data rows. All nine are wet-season windows: 2003-01-30 (2 days), 2011-01-30
(2 days), 2017-01-25 (5 days), 2020-11-26 (5 days), 2021-01-10 (5 days), 2021-12-31
(5 days), 2023-01-25 (5 days), 2025-01-20 (5 days), and 2025-12-31 (5 days).

The saved responses are valid CSV files with the standard column header and no data rows.
`src/fetch_firms.py` accepts only response bodies that begin with `latitude`; an HTTP error
or an error message would not have that form and would have raised after the retry loop.
NASA FIRMS also maintains a separate missing-data table for days when a satellite
instrument has no data. On 2 November 2026 that table at
`https://firms.modaps.eosdis.nasa.gov/api/missing_data/` contained no missing MODIS
Terra or Aqua date in any of the nine windows above. The empty files therefore mean zero
detections in the requested box and window, not missing satellite data.

## 8. Review fixes carried in this branch

1. `src/v2_q3.py` now leaves `factor_unit` empty for the two `context post2016 step`
   rows, where `factor_less_rain` is not defined and the rain-unit label was misleading.
   The script was rerun; every numeric column in `results/v2_q3_results.csv` is unchanged.
2. The empty `firms_v2` files are documented in section 7 above, with the FIRMS
   missing-data check recorded.

## 9. Deviations and implementation notes

No deviation from the frozen plan was needed for Step 0. Two implementation choices were
not fixed by the plan text:

- the equal-area grid uses the MODIS sinusoidal projection, with 1 km cells;
- when a Dryad event has detections in more than one box, it is assigned to the box that
  holds the most of its detections. No kept event has a Dryad `Island` code that
  contradicts its coordinate-based box.

The `docs/research_plan_v2.md` Deviations section is left unchanged because these choices
do not alter the plan's definitions or the pass criterion.
