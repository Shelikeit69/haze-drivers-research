# Haze drivers research

[中文版](README.zh-CN.md)

**Since 2016 Indonesia burns far less for the same amount of rain, but an El Niño summer still means a drier fire season, more fires and worse haze in Singapore.**

Read the short paper: [docs/paper_climate_fire_singapore_haze_2026-10-16.pdf](docs/paper_climate_fire_singapore_haze_2026-10-16.pdf) (12 pages, 6 figures).

## Main numbers

All five planned tests hold after Holm correction for multiple testing.

| Link | Result | Years |
|---|---|---|
| El Niño (ONI, June to August) and Kalimantan rain (August to October) | r = −0.79 | 1979 to 2025 |
| Indian Ocean Dipole and Sumatra rain, El Niño held fixed | 1.7 mm/day less rain per 1 °C | 1979 to 2025 |
| Rain and fire detections, policy period held fixed | 1 mm/day less rain: 1.55× fires in Sumatra, 1.44× in Kalimantan | 2001 to 2025 |
| Fires since 2016 at the same rain | about 77% fewer in Sumatra, 47% fewer in Kalimantan | 2001 to 2025 |
| Fire detections and Singapore PM2.5 | Spearman ρ = 0.88 | 2016 to 2025 (10 seasons) |

## Limits

- The June to August indices are published in September. They warn ahead of September and October, which held 67% of August to October fire detections in 2001 to 2025, but not before the season starts.
- The Singapore link rests on ten seasons and does not include 2015.
- The tests were run on data that had already been explored, so this is not a pre-registered study.
- These are yearly correlations. They do not prove cause, and nothing here forecasts 2027.
- This is a personal project. It has not been peer reviewed.

Separate from the AI4Climate entry `sg-haze-window`. Nothing here feeds that product.

## Layout

| Path | What it is |
|---|---|
| `data/raw/` | Raw API responses, saved unchanged. **Read-only**: never edit; all cleaning happens in code. `SHA256SUMS.txt` lets you check nothing changed (`cd data/raw && sha256sum -c SHA256SUMS.txt`). |
| `src/fetch.py` | Downloads the raw data (skips files that already exist). |
| `src/analyse.py` | Round 1: builds the SOI, seasonal rain and Singapore haze metrics; runs the correlations. |
| `src/analyse_r2.py` | Round 2: official ONI cross-check and the Indian Ocean Dipole. Reads round-1 results, so run after `analyse.py`. |
| `src/analyse_r3.py` | Round 3: re-test with GPCP rainfall (independent of ERA5). Run after `analyse_r2.py`. Needs `netCDF4`. |
| `src/fetch_firms.py` | Downloads NASA FIRMS MODIS fire detections. Reads the key from `FIRMS_MAP_KEY`; the key is never stored. |
| `src/analyse_r4.py` | Round 4: drought → fires → Singapore PM2.5. Run after `analyse_r3.py`. |
| `src/plot_r4.py` | Draws `results/fires_r4.png`. |
| `src/confirmatory.py` | Primary tests and robustness checks under `docs/research_plan_v1.md`. Run after `analyse_r4.py`. Needs `statsmodels`. |
| `src/fire_months.py` | Share of Aug–Oct fire detections by month (used for the timing statement in the paper). |
| `src/plot.py` | Draws `results/enso_haze.png`. |
| `results/` | Outputs of the current code. Regenerate rather than edit. |
| `docs/` | The paper (PDF), the frozen research plan, the literature review and one findings note per analysis round. |
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
```

Needs Python 3 with pandas, numpy, scipy, matplotlib, netCDF4, statsmodels. Re-downloading (`python src/fetch.py data/raw`) is only needed to extend the data; it will not overwrite existing files.

## Licence and attribution

Code, notes and the paper in this repo are released under the MIT licence (`LICENSE`), copyright Zhang Lin Si Cheng.

Files in `data/raw/` are copies of third-party data and are not covered by the MIT licence. Each keeps the terms in the table below. If you reuse them, credit the original source:

- Singapore PSI and PM2.5: contains information from the PSI dataset accessed on 16 Oct 2026 from data.gov.sg, made available under the Singapore Open Data Licence version 1.0.
- ERA5 rain and pressure: weather data by Open-Meteo.com (CC BY 4.0), based on Copernicus Climate Change Service ERA5 reanalysis.
- ONI, DMI and GPCP: NOAA Physical Sciences Laboratory. HadISST (behind the DMI) is Met Office data. Cite Adler et al. (2003) for GPCP.
- Fire detections: NASA FIRMS (MODIS standard product for 2001 to 2025, near-real-time product for 2026).

## Data sources (downloaded 16 Oct 2026)

| Data | Source | Coverage in this repo | Licence |
|---|---|---|---|
| Daily mean sea-level pressure, daily precipitation (ERA5 reanalysis) | Open-Meteo Historical Weather API | 1950-01-01 to 2026-10-10, 8 points (below) | CC BY 4.0; free for non-commercial use |
| ONI (CPC, ERSST v6, 3-month running mean; file says "as of 09/7/2026") | NOAA PSL `psl.noaa.gov/data/correlation/oni.data`, downloaded by Toni, saved as `noaa_psl_oni.data` | Jan 1950 to Aug 2026 (centre month) | US government data |
| Dipole Mode Index (HadISST1.1; created 25 Jul 2026, recent months preliminary) | NOAA PSL `psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data`, downloaded by Toni, saved as `noaa_psl_dmi_had_long.data` | Jan 1870 to May 2026 | NOAA PSL; HadISST is Met Office data, credit required |
| GPCP v2.3 monthly precipitation, 2.5° (satellite + gauge; Nov 2021 onward interim) | NOAA PSL `downloads.psl.noaa.gov/Datasets/gpcp/precip.mon.mean.nc`, downloaded by Toni, saved as `noaa_psl_gpcp_v2.3_precip.mon.mean.nc` | Jan 1979 to Jun 2026 | NOAA PSL; cite Adler et al. 2003 (citation in file) |
| MODIS active-fire detections (MODIS_SP 2001–2025; MODIS_NRT 2026) | NASA FIRMS area API, box 100–116.5°E, 5°S–2.3°N, downloaded 16 Oct 2026 with Toni's MAP_KEY | 1 Aug–31 Oct 2001–2025; 1 Aug–15 Oct 2026 | NASA open data; cite FIRMS |
| PSI and 24-h PM2.5 by region, hourly | NEA via data.gov.sg real-time API (`/v2/real-time/api/psi?date=`) | 1 Aug–31 Oct, 2016–2025; 1 Aug–15 Oct 2026 | Singapore Open Data Licence; credit source, do not imply official status |

ERA5 points (requested lat, lon; Open-Meteo snaps to the nearest grid cell, actual cell recorded in each JSON):

- SOI stations: Darwin (-12.46, 130.84), Tahiti (-17.53, -149.57)
- Sumatra: Riau (0.50, 101.50), Jambi (-1.60, 103.60), South Sumatra (-3.00, 104.80)
- Kalimantan: West (-0.50, 109.50), Central (-2.20, 113.90), South (-3.30, 114.60)

## Method notes

- **Headline pair from round 3 on: official ONI with GPCP rain.** Round 3 showed part of SOI's apparent advantage came from SOI and ERA5 rain sharing a source.
- **Round 1 ENSO index = SOI computed here.** NOAA's site could not be reached from the work environment; the official ONI was added in round 2 as a cross-check. SOI uses the Troup formula on ERA5 monthly Tahiti minus Darwin pressure, 1981–2010 base. Negative = El Niño. It is not the official Bureau of Meteorology SOI series.
- **Singapore metrics are rebuilt from the five regions** for every year, because the `national` field disappears from 2024. PSI = max over regions (NEA's national definition); PM2.5 = mean over the regions reporting that hour.
- Seasonal rain = mean of the three points per island, Aug–Oct, mm/day. A season with any missing day is left blank.

## Known data problems (kept, not filled)

- NEA API has no data before 2016, so the 2015 haze is not in the Singapore series.
- NEA returns "data not found" for 20 days: 2019-08-09, 08-15, 09-06, 09-10, 09-11, 09-14, 09-15, 09-21, 09-25, 09-26, 10-02, 10-17, 10-18; 2021-10-01 to 10-04, 10-25; 2023-10-08, 10-31. Several 2019 gaps fall on peak haze days, so 2019 haze is understated. Some other days have fewer than 24 hourly readings.
- ERA5 values for recent months are preliminary and can be revised. ERA5 tropical rainfall is biased; the 4 mm/day threshold from Field et al. (TRMM-based) is shown for reference only.
- 2026 rain is incomplete (to 10 Oct), so 2026 enters only the "same window" test (1 Aug–10 Oct).
