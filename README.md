# Haze drivers research

[中文版](README.zh-CN.md)

**Since 2016 Indonesia burns far less for the same amount of rain, but an El Niño summer still means a drier fire season, more fires and worse haze in Singapore.**

The short paper is here: [docs/paper_climate_fire_singapore_haze_2026-10-16.pdf](docs/paper_climate_fire_singapore_haze_2026-10-16.pdf) (13 pages, 6 figures; revised 19 Oct 2026).

## v2 (November 2026)

v2 grew out of two suggestions from Dr Sean Sloan (Vancouver Island University), whose own work (Sloan et al. 2022, *Communications Earth & Environment* 3:207, doi 10.1038/s43247-022-00522-6) measured fire severity at the level of fire events and controlled for fire-season rain. Dr Sloan suggested: (1) use the sum of fire radiative power (FRP) instead of detection counts for fire severity, and (2) start the rain accumulation one to two months before the fire season, because rain acts non-linearly and over a longer window. v2 also replicates Sloan et al.'s event-based trend analysis on our two-island region.

The main numbers, all drawn from the conclusions note, are:

- **Step 0 replication of Sloan's fire events.** Our events, built with his definitions on our island boxes, produce severe-event time series that correlate at Pearson r = 0.9995 on Sumatra and 0.99998 on Kalimantan with his published Dryad events; the 18-season totals are within 1.5 percent. Two differences remain between our construction and his: FIRMS Collection 6.1 (we use) against 6 (he used), and our events can run from December into January where his stop at the calendar year.
- **Q1, 2002–2019 replication.** Severe-event share declines on both islands (Sumatra −11.7 percent, Kalimantan −17.7 percent), in the same direction as Sloan's four-region range (−19 to −27 percent). Very-severe-event share declines in Kalimantan (−30.1 percent, inside his range) but not in Sumatra (+2.3 percent, with a wide bootstrap interval).
- **Q2, decline to 2025.** Controlling for Jul–Dec rain, the share of fire events that are severe falls by 0.0038 a year in Sumatra (p = 0.0028, −22.5 percent over 17 years) and 0.0041 a year in Kalimantan (p = 0.00004, −21.5 percent over 17 years). All six confirmatory tests (T1 to T6) stay significant after the Holm correction.
- **Q3, v1 rain-fire link with Sloan's suggestions.** The link holds when fire is measured by FRP sum and when rain is cumulative from June. Aug–Oct FRP sum increases by a factor of 1.59 (Sumatra) and 1.47 (Kalimantan) per 1 mm/day less Aug–Oct rain, and by 1.51 and 1.36 per 100 mm less Jun–Oct rain. The Spearman correlation between the two islands' Aug–Oct FRP sum and Singapore's Aug–Oct mean PM2.5 is 0.93 over 2016 to 2025 (10 seasons).

Full write-up: [docs/2026-11-02_v2_conclusions.md](docs/2026-11-02_v2_conclusions.md). Frozen plan: [docs/research_plan_v2.md](docs/research_plan_v2.md).

## Main numbers (v1)

All five planned tests hold after Holm correction for multiple testing.

| Link | Result | Years |
|---|---|---|
| El Niño (ONI, June to August) and Kalimantan rain (August to October) | r = −0.79 | 1979 to 2025 |
| Indian Ocean Dipole and Sumatra rain, El Niño held fixed | 1.7 mm/day less rain per 1 °C | 1979 to 2025 |
| Rain and fire detections, policy period held fixed | 1 mm/day less rain: 1.55× fires in Sumatra, 1.44× in Kalimantan | 2001 to 2025 |
| Fires since 2016 at the same rain, with the break set at 2016 | about 77% fewer in Sumatra, 47% fewer in Kalimantan (49% to 79% and 18% to 47% fewer for breaks from 2008 to 2021) | 2001 to 2025 |
| Fire detections and Singapore PM2.5 | Spearman ρ = 0.88 | 2016 to 2025 (10 seasons) |

## Limits

v1:

- The June to August indices come out in September. That is before September and October, which held 67% of August to October fire detections in 2001 to 2025, but it is after the season has started.
- The size of the post-2015 drop depends on which year the break is put in. The rain effect does not.
- The Singapore link rests on ten seasons and leaves out 2015.
- I ran the tests on data I had already explored, so this is not a pre-registered study.
- These are yearly correlations. They do not prove cause, and nothing here forecasts 2027.
- This is a personal project and has not been peer reviewed.

v2:

- The evidence is correlational, from 24 seasons (10 for the Singapore link).
- The plan was written after the Aug–Oct counts and FRP totals had been seen, so it is not a pre-registration (see the plan's honesty statement).
- Rain comes from GPCP at 2.5 degrees, three cells per island. The CHIRPS check and the VIIRS check in the plan were not run.
- Rain enters the models linearly. A LOWESS curve of fire energy against Jul–Dec rain falls gradually and flattens at high rain, with no sharp threshold, but no threshold test was run.
- Sumatra's very severe share is the one replication result that does not match Sloan's direction.

It is separate from my AI4Climate entry `sg-haze-window`, and nothing here feeds that product.

## Layout

| Path | What it is |
|---|---|
| `data/raw/` | Raw API responses, saved unchanged. Treat them as read-only: all cleaning happens in code. `SHA256SUMS.txt` lets you check that nothing changed (`cd data/raw && sha256sum -c SHA256SUMS.txt`). |
| `data/external/sloan_dryad/` | Manual copy of Sloan et al.'s Dryad event tables (doi 10.5061/dryad.msbcc2g1t). Ignored by git because the zip is above GitHub's file size limit. `src/v2_step0.py` reads CSVs from the fixed subpath `data/external/sloan_dryad/Dryad_Version_ofGDB/`. |
| `src/fetch.py` | Downloads the raw data and skips files that already exist. |
| `src/analyse.py` | Round 1. Builds the SOI, seasonal rain and Singapore haze metrics, then runs the correlations. |
| `src/analyse_r2.py` | Round 2. Cross-checks with the official ONI and adds the Indian Ocean Dipole. Reads round 1 results, so run it after `analyse.py`. |
| `src/analyse_r3.py` | Round 3. Repeats the tests with GPCP rain, which does not depend on ERA5. Run after `analyse_r2.py`. Needs `netCDF4`. |
| `src/fetch_firms.py` | Downloads NASA FIRMS MODIS fire detections for the Aug–Oct window (v1). It reads the key from `FIRMS_MAP_KEY` and never stores it. |
| `src/fetch_firms_v2.py` | Downloads NASA FIRMS MODIS_SP fire detections for 1 Jun to 31 Jul and 1 Nov to 31 Jan of the next year, 2002 to 2025 (edge months needed for event construction; Aug to Oct comes from `data/raw/firms/`). Reads the key from `FIRMS_MAP_KEY`. |
| `src/analyse_r4.py` | Round 4. Drought, fires and Singapore PM2.5. Run after `analyse_r3.py`. |
| `src/plot_r4.py` | Draws `results/fires_r4.png`. |
| `src/confirmatory.py` | Primary tests and robustness checks from `docs/research_plan_v1.md`. Run after `analyse_r4.py`. Needs `statsmodels`. |
| `src/fire_months.py` | Monthly share of August to October fire detections. The paper's timing statement comes from this. |
| `src/posthoc_checks.py` | Post-hoc checks after reviewer feedback (negative binomial, first differences, stationarity). Outside the frozen plan. |
| `src/plot.py` | Draws `results/enso_haze.png`. |
| `src/v2_step0.py` | Builds Sloan-style fire events from FIRMS detections and validates them against the Dryad tables. Reads Sloan's Dryad CSVs from the fixed path `data/external/sloan_dryad/Dryad_Version_ofGDB/`. |
| `src/v2_q3.py` | v1 rain-fire link re-run with Sloan's suggestions (FRP sum, cumulative rain). Runs on data already in the repo. |
| `src/v2_stage2.py` | v2 Step 1 replication, T1–T2 confirmatory tests, Holm correction, robustness checks, exploratory analyses. Builds events via `v2_step0.build_events` on already-downloaded FIRMS data; does not read the Dryad data. |
| `src/v2_figures.py` | Draws the Step 0 replication figure used in `docs/2026-11-02_v2_conclusions.md`. Reads only `results/` files; does not re-run any model. |
| `results/` | Output of the current code. Rerun the code instead of editing these files. |
| `docs/` | The paper (PDF), the frozen research plans (v1 and v2), the literature review, the v2 conclusion and result notes, and one note per v1 analysis round. |
| `LICENSE` | MIT licence for the code and text written here. Raw data keep their own licences (see below). |

## Reproduce

v1:

```
python src/analyse.py data/raw results
python src/analyse_r2.py data/raw results
python src/analyse_r3.py data/raw results
python src/analyse_r4.py data/raw results
python src/plot_r4.py results
python src/confirmatory.py results
python src/fire_months.py data/raw results
python src/plot.py results
python src/posthoc_checks.py results
```

v2, run after v1 (the v2 event builder reuses the v1 FIRMS files):

1. **Dryad data (manual download, 202 MB, above GitHub's file limit).** Open `https://datadryad.org/dataset/doi:10.5061/dryad.msbcc2g1t` in a browser and click "Download full dataset". Check the SHA256 of the zip:

   ```
   sha256sum doi_10_5061_dryad_msbcc2g1t__v20220828.zip
   # expect: 0b76226376a13cc8212df0f07041597cd169fba9c7cbdcd8cb6541e80a789e3b
   ```

   The outer zip contains `Dryad_Version_ofGDB.zip`, which itself holds the CSVs that `src/v2_step0.py` reads from the fixed path `data/external/sloan_dryad/Dryad_Version_ofGDB/`:

   ```
   mkdir -p data/external/sloan_dryad
   unzip doi_10_5061_dryad_msbcc2g1t__v20220828.zip -d data/external/sloan_dryad
   cd data/external/sloan_dryad
   unzip Dryad_Version_ofGDB.zip
   cd /workspace
   ```

2. **FIRMS key (read from environment, never written to disk).** Set `FIRMS_MAP_KEY` in your shell. `src/fetch_firms_v2.py` needs it. The v2 analysis scripts (`v2_step0.py`, `v2_stage2.py`) read already-downloaded FIRMS files from disk and do not call the FIRMS API.

3. **Scripts, in order:**

   ```
   python src/fetch_firms_v2.py data/raw/firms_v2
   python src/v2_q3.py data/raw results
   python src/v2_step0.py data/raw results
   python src/v2_stage2.py data/raw results
   python src/v2_figures.py results
   ```

   `v2_q3.py` does not need the Dryad data and can be run any time after the v1 FIRMS files are in place. `v2_step0.py` reads Sloan's Dryad CSVs from `data/external/sloan_dryad/Dryad_Version_ofGDB/`. `v2_stage2.py` does not read the Dryad data; it builds events with `v2_step0.build_events` on FIRMS detections already present in `data/raw/firms` and `data/raw/firms_v2`. `v2_figures.py` needs only the `results/` files produced by the earlier scripts.

You need Python 3 with pandas, numpy, scipy, matplotlib, netCDF4 and statsmodels.

## Licence and attribution

The code, notes and paper in this repo are released under the MIT licence (`LICENSE`), copyright Zhang Lin Si Cheng.

Files in `data/raw/` are copies of third-party data. The MIT licence does not cover them; each keeps the terms in the table below. If you reuse them, credit the source:

- Singapore PSI and PM2.5: contains information from the PSI dataset accessed on 16 Oct 2026 from data.gov.sg, made available under the Singapore Open Data Licence version 1.0.
- ERA5 rain and pressure: weather data by Open-Meteo.com (CC BY 4.0), based on the Copernicus Climate Change Service ERA5 reanalysis.
- ONI, DMI and GPCP: NOAA Physical Sciences Laboratory. HadISST, which the DMI is built on, is Met Office data. Cite Adler et al. (2003) for GPCP.
- Fire detections: NASA FIRMS (MODIS standard product for 2001 to 2025, near-real-time product for 2026).
- Sloan et al. event data: see the Dryad page for the licence (doi 10.5061/dryad.msbcc2g1t).

## Data sources

| Data | Source | Coverage in this repo | Licence |
|---|---|---|---|
| Daily mean sea-level pressure and daily precipitation (ERA5 reanalysis) | Open-Meteo Historical Weather API | 1 Jan 1950 to 10 Oct 2026, 8 points (listed below) | CC BY 4.0; free for non-commercial use |
| ONI (CPC, ERSST v6, 3-month running mean; the file says "as of 09/7/2026") | NOAA PSL `psl.noaa.gov/data/correlation/oni.data`, downloaded by Toni and saved as `noaa_psl_oni.data` | Jan 1950 to Aug 2026 (centre month) | US government data |
| Dipole Mode Index (HadISST1.1; created 25 Jul 2026; recent months are preliminary) | NOAA PSL `psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data`, downloaded by Toni and saved as `noaa_psl_dmi_had_long.data` | Jan 1870 to May 2026 | NOAA PSL; HadISST is Met Office data and needs credit |
| GPCP v2.3 monthly precipitation, 2.5° grid (satellite plus rain gauge; interim from Nov 2021) | NOAA PSL `downloads.psl.noaa.gov/Datasets/gpcp/precip.mon.mean.nc`, downloaded by Toni and saved as `noaa_psl_gpcp_v2.3_precip.mon.mean.nc` | Jan 1979 to Jun 2026 | NOAA PSL; cite Adler et al. 2003 (citation in the file) |
| MODIS active-fire detections, Aug–Oct 2001–2025 and near-real-time 2026 | NASA FIRMS area API, box 100 to 116.5°E and 5°S to 2.3°N, downloaded 16 Oct 2026 with Toni's MAP_KEY (v1, saved under `data/raw/firms/`) | 1 Aug to 31 Oct 2001–2025; 1 Aug to 15 Oct 2026 | NASA open data; cite FIRMS |
| MODIS active-fire detections, 1 Jun–31 Jul and 1 Nov–31 Jan 2002–2025 (edge months for v2 event construction; Aug–Oct for these seasons comes from `data/raw/firms/`) | NASA FIRMS area API, same box, downloaded 2 Nov 2026 (saved under `data/raw/firms_v2/`) | 1 Jun to 31 Jul and 1 Nov to 31 Jan of the next year, for the 2002 to 2025 seasons; Aug to Oct comes from `data/raw/firms/` | NASA open data; cite FIRMS |
| Sloan et al. fire-event detections and ignitions, 2002–2019 | Dryad doi 10.5061/dryad.msbcc2g1t, version of 28 Aug 2022, downloaded manually | Fire-event detections and ignitions for Indonesia, 2002 to 2019 | Check the Dryad page |
| Hourly PSI and 24-hour PM2.5 by region | NEA via the data.gov.sg real-time API (`/v2/real-time/api/psi?date=`) | 1 Aug to 31 Oct 2016–2025; 1 Aug to 15 Oct 2026 | Singapore Open Data Licence; credit the source and do not imply official status |

ERA5 points, as requested latitude and longitude. Open-Meteo snaps each one to the nearest grid cell, and each JSON file records the cell it used.

- SOI stations: Darwin (-12.46, 130.84), Tahiti (-17.53, -149.57)
- Sumatra: Riau (0.50, 101.50), Jambi (-1.60, 103.60), South Sumatra (-3.00, 104.80)
- Kalimantan: West (-0.50, 109.50), Central (-2.20, 113.90), South (-3.30, 114.60)

## Method notes

- From round 3 on, the main pair is the official ONI with GPCP rain. Round 3 showed that part of the SOI's apparent edge came from the SOI and ERA5 rain sharing a source.
- Round 1 used an SOI computed here, because NOAA's site could not be reached from the work environment at the time. The official ONI came in at round 2 as a cross-check. The SOI uses the Troup formula on ERA5 monthly Tahiti minus Darwin pressure, with a 1981 to 2010 base. Negative values mean El Niño. It is not the Bureau of Meteorology's official SOI.
- Singapore metrics are rebuilt from the five regions for every year, because the API drops the `national` field from 2024. PSI is the maximum over regions, which is how NEA defines the national value. PM2.5 is the mean over the regions reporting in that hour.
- Seasonal rain is the mean of the three points on each island over August to October, in mm/day. A season with any missing day is left blank.
- v2 event construction uses the MODIS sinusoidal projection, a 1 km equal-area grid, 8-neighbour adjacency, and all MODIS detection types. Events igniting outside Jul–Dec are dropped, and events can run from December into the following January (unlike Sloan et al.'s calendar-year stop).

## Known data problems (kept, not filled)

- The NEA API has no data before 2016, so the 2015 haze is missing from the Singapore series.
- NEA returns "data not found" for 20 days: 2019-08-09, 08-15, 09-06, 09-10, 09-11, 09-14, 09-15, 09-21, 09-25, 09-26, 10-02, 10-17, 10-18; 2021-10-01 to 10-04, 10-25; 2023-10-08, 10-31. Several of the 2019 gaps fall on peak haze days, so 2019 haze is understated. Some other days have fewer than 24 hourly readings.
- ERA5 values for recent months are preliminary and may be revised. ERA5 tropical rain is biased, so the 4 mm/day threshold from Field et al. (based on TRMM) is shown for reference only.
- 2026 rain runs only to 10 Oct, so 2026 appears only in the same-window comparison (1 Aug to 10 Oct).
- v2 FIRMS files downloaded 2 Nov 2026 include nine empty (zero-row) MODIS_SP files, all from wet-season windows. They are documented in `results/v2_step0_empty_firms_v2.csv`.
