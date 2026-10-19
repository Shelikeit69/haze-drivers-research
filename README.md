# Haze drivers research

[中文版](README.zh-CN.md)

**Since 2016 Indonesia burns far less for the same amount of rain, but an El Niño summer still means a drier fire season, more fires and worse haze in Singapore.**

The short paper is here: [docs/paper_climate_fire_singapore_haze_2026-10-16.pdf](docs/paper_climate_fire_singapore_haze_2026-10-16.pdf) (13 pages, 6 figures; revised 19 Oct 2026).

## Main numbers

All five planned tests hold after Holm correction for multiple testing.

| Link | Result | Years |
|---|---|---|
| El Niño (ONI, June to August) and Kalimantan rain (August to October) | r = −0.79 | 1979 to 2025 |
| Indian Ocean Dipole and Sumatra rain, El Niño held fixed | 1.7 mm/day less rain per 1 °C | 1979 to 2025 |
| Rain and fire detections, policy period held fixed | 1 mm/day less rain: 1.55× fires in Sumatra, 1.44× in Kalimantan | 2001 to 2025 |
| Fires since 2016 at the same rain, with the break set at 2016 | about 77% fewer in Sumatra, 47% fewer in Kalimantan (49% to 79% and 18% to 47% fewer for breaks from 2008 to 2021) | 2001 to 2025 |
| Fire detections and Singapore PM2.5 | Spearman ρ = 0.88 | 2016 to 2025 (10 seasons) |

## Limits

- The June to August indices come out in September. That is before September and October, which held 67% of August to October fire detections in 2001 to 2025, but it is after the season has started.
- The size of the post-2015 drop depends on which year the break is put in. The rain effect does not.
- The Singapore link rests on ten seasons and leaves out 2015.
- I ran the tests on data I had already explored, so this is not a pre-registered study.
- These are yearly correlations. They do not prove cause, and nothing here forecasts 2027.
- This is a personal project and has not been peer reviewed.

It is separate from my AI4Climate entry `sg-haze-window`, and nothing here feeds that product.

## Layout

| Path | What it is |
|---|---|
| `data/raw/` | Raw API responses, saved unchanged. Treat them as read-only: all cleaning happens in code. `SHA256SUMS.txt` lets you check that nothing changed (`cd data/raw && sha256sum -c SHA256SUMS.txt`). |
| `src/fetch.py` | Downloads the raw data and skips files that already exist. |
| `src/analyse.py` | Round 1. Builds the SOI, seasonal rain and Singapore haze metrics, then runs the correlations. |
| `src/analyse_r2.py` | Round 2. Cross-checks with the official ONI and adds the Indian Ocean Dipole. Reads round 1 results, so run it after `analyse.py`. |
| `src/analyse_r3.py` | Round 3. Repeats the tests with GPCP rain, which does not depend on ERA5. Run after `analyse_r2.py`. Needs `netCDF4`. |
| `src/fetch_firms.py` | Downloads NASA FIRMS MODIS fire detections. It reads the key from `FIRMS_MAP_KEY` and never stores it. |
| `src/analyse_r4.py` | Round 4. Drought, fires and Singapore PM2.5. Run after `analyse_r3.py`. |
| `src/plot_r4.py` | Draws `results/fires_r4.png`. |
| `src/confirmatory.py` | Primary tests and robustness checks from `docs/research_plan_v1.md`. Run after `analyse_r4.py`. Needs `statsmodels`. |
| `src/fire_months.py` | Monthly share of August to October fire detections. The paper's timing statement comes from this. |
| `src/posthoc_checks.py` | Post-hoc checks after reviewer feedback (negative binomial, first differences, stationarity). Outside the frozen plan. |
| `src/plot.py` | Draws `results/enso_haze.png`. |
| `results/` | Output of the current code. Rerun the code instead of editing these files. |
| `docs/` | The paper (PDF), the frozen research plan, the literature review and one note per analysis round. |
| `LICENSE` | MIT licence for the code and text written here. Raw data keep their own licences (see below). |

## Reproduce

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

You need Python 3 with pandas, numpy, scipy, matplotlib, netCDF4 and statsmodels. You only need to download again (`python src/fetch.py data/raw`) to add new data. Existing files are not overwritten.

## Licence and attribution

The code, notes and paper in this repo are released under the MIT licence (`LICENSE`), copyright Zhang Lin Si Cheng.

Files in `data/raw/` are copies of third-party data. The MIT licence does not cover them; each keeps the terms in the table below. If you reuse them, credit the source:

- Singapore PSI and PM2.5: contains information from the PSI dataset accessed on 16 Oct 2026 from data.gov.sg, made available under the Singapore Open Data Licence version 1.0.
- ERA5 rain and pressure: weather data by Open-Meteo.com (CC BY 4.0), based on the Copernicus Climate Change Service ERA5 reanalysis.
- ONI, DMI and GPCP: NOAA Physical Sciences Laboratory. HadISST, which the DMI is built on, is Met Office data. Cite Adler et al. (2003) for GPCP.
- Fire detections: NASA FIRMS (MODIS standard product for 2001 to 2025, near-real-time product for 2026).

## Data sources (downloaded 16 Oct 2026)

| Data | Source | Coverage in this repo | Licence |
|---|---|---|---|
| Daily mean sea-level pressure and daily precipitation (ERA5 reanalysis) | Open-Meteo Historical Weather API | 1 Jan 1950 to 10 Oct 2026, 8 points (listed below) | CC BY 4.0; free for non-commercial use |
| ONI (CPC, ERSST v6, 3-month running mean; the file says "as of 09/7/2026") | NOAA PSL `psl.noaa.gov/data/correlation/oni.data`, downloaded by Toni and saved as `noaa_psl_oni.data` | Jan 1950 to Aug 2026 (centre month) | US government data |
| Dipole Mode Index (HadISST1.1; created 25 Jul 2026; recent months are preliminary) | NOAA PSL `psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data`, downloaded by Toni and saved as `noaa_psl_dmi_had_long.data` | Jan 1870 to May 2026 | NOAA PSL; HadISST is Met Office data and needs credit |
| GPCP v2.3 monthly precipitation, 2.5° grid (satellite plus rain gauge; interim from Nov 2021) | NOAA PSL `downloads.psl.noaa.gov/Datasets/gpcp/precip.mon.mean.nc`, downloaded by Toni and saved as `noaa_psl_gpcp_v2.3_precip.mon.mean.nc` | Jan 1979 to Jun 2026 | NOAA PSL; cite Adler et al. 2003 (citation in the file) |
| MODIS active-fire detections (MODIS_SP for 2001 to 2025, MODIS_NRT for 2026) | NASA FIRMS area API, box 100 to 116.5°E and 5°S to 2.3°N, downloaded 16 Oct 2026 with Toni's MAP_KEY | 1 Aug to 31 Oct in 2001 to 2025; 1 Aug to 15 Oct 2026 | NASA open data; cite FIRMS |
| Hourly PSI and 24-hour PM2.5 by region | NEA via the data.gov.sg real-time API (`/v2/real-time/api/psi?date=`) | 1 Aug to 31 Oct in 2016 to 2025; 1 Aug to 15 Oct 2026 | Singapore Open Data Licence; credit the source and do not imply official status |

ERA5 points, as requested latitude and longitude. Open-Meteo snaps each one to the nearest grid cell, and each JSON file records the cell it used.

- SOI stations: Darwin (-12.46, 130.84), Tahiti (-17.53, -149.57)
- Sumatra: Riau (0.50, 101.50), Jambi (-1.60, 103.60), South Sumatra (-3.00, 104.80)
- Kalimantan: West (-0.50, 109.50), Central (-2.20, 113.90), South (-3.30, 114.60)

## Method notes

- From round 3 on, the main pair is the official ONI with GPCP rain. Round 3 showed that part of the SOI's apparent edge came from the SOI and ERA5 rain sharing a source.
- Round 1 used an SOI computed here, because NOAA's site could not be reached from the work environment at the time. The official ONI came in at round 2 as a cross-check. The SOI uses the Troup formula on ERA5 monthly Tahiti minus Darwin pressure, with a 1981 to 2010 base. Negative values mean El Niño. It is not the Bureau of Meteorology's official SOI.
- Singapore metrics are rebuilt from the five regions for every year, because the API drops the `national` field from 2024. PSI is the maximum over regions, which is how NEA defines the national value. PM2.5 is the mean over the regions reporting in that hour.
- Seasonal rain is the mean of the three points on each island over August to October, in mm/day. A season with any missing day is left blank.

## Known data problems (kept, not filled)

- The NEA API has no data before 2016, so the 2015 haze is missing from the Singapore series.
- NEA returns "data not found" for 20 days: 2019-08-09, 08-15, 09-06, 09-10, 09-11, 09-14, 09-15, 09-21, 09-25, 09-26, 10-02, 10-17, 10-18; 2021-10-01 to 10-04, 10-25; 2023-10-08, 10-31. Several of the 2019 gaps fall on peak haze days, so 2019 haze is understated. Some other days have fewer than 24 hourly readings.
- ERA5 values for recent months are preliminary and may be revised. ERA5 tropical rain is biased, so the 4 mm/day threshold from Field et al. (based on TRMM) is shown for reference only.
- 2026 rain runs only to 10 Oct, so 2026 appears only in the same-window comparison (1 Aug to 10 Oct).
