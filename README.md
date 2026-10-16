# Haze drivers research

What drives the Indonesia-to-Singapore haze season? This repo tests the climate link first (El Niño → Indonesian dry-season rain → Singapore haze). Crop economics (palm oil prices, biodiesel mandates, replanting cycles) come later.

Separate from the AI4Climate entry `sg-haze-window`. Nothing here feeds that product.

## Layout

| Path | What it is |
|---|---|
| `data/raw/` | Raw API responses, saved unchanged. **Read-only**: never edit; all cleaning happens in code. `SHA256SUMS.txt` lets you check nothing changed (`cd data/raw && sha256sum -c SHA256SUMS.txt`). |
| `src/fetch.py` | Downloads the raw data (skips files that already exist). |
| `src/analyse.py` | Round 1: builds the SOI, seasonal rain and Singapore haze metrics; runs the correlations. |
| `src/analyse_r2.py` | Round 2: official ONI cross-check and the Indian Ocean Dipole. Reads round-1 results, so run after `analyse.py`. |
| `src/plot.py` | Draws `results/enso_haze.png`. |
| `results/` | Outputs of the current code. Regenerate rather than edit. |
| `docs/` | Findings notes, one per analysis round. |

## Reproduce

```
python src/analyse.py data/raw results
python src/analyse_r2.py data/raw results
python src/plot.py results
```

Needs Python 3 with pandas, numpy, scipy, matplotlib. Re-downloading (`python src/fetch.py data/raw`) is only needed to extend the data; it will not overwrite existing files.

## Data sources (downloaded 16 Oct 2026)

| Data | Source | Coverage in this repo | Licence |
|---|---|---|---|
| Daily mean sea-level pressure, daily precipitation (ERA5 reanalysis) | Open-Meteo Historical Weather API | 1950-01-01 to 2026-10-10, 8 points (below) | CC BY 4.0; free for non-commercial use |
| ONI (CPC, ERSST v6, 3-month running mean; file says "as of 09/7/2026") | NOAA PSL `psl.noaa.gov/data/correlation/oni.data`, downloaded by Toni, saved as `noaa_psl_oni.data` | Jan 1950 to Aug 2026 (centre month) | US government data |
| Dipole Mode Index (HadISST1.1; created 25 Jul 2026, recent months preliminary) | NOAA PSL `psl.noaa.gov/gcos_wgsp/Timeseries/Data/dmi.had.long.data`, downloaded by Toni, saved as `noaa_psl_dmi_had_long.data` | Jan 1870 to May 2026 | NOAA PSL; HadISST is Met Office data, credit required |
| PSI and 24-h PM2.5 by region, hourly | NEA via data.gov.sg real-time API (`/v2/real-time/api/psi?date=`) | 1 Aug–31 Oct, 2016–2025; 1 Aug–15 Oct 2026 | Singapore Open Data Licence; credit source, do not imply official status |

ERA5 points (requested lat, lon; Open-Meteo snaps to the nearest grid cell, actual cell recorded in each JSON):

- SOI stations: Darwin (-12.46, 130.84), Tahiti (-17.53, -149.57)
- Sumatra: Riau (0.50, 101.50), Jambi (-1.60, 103.60), South Sumatra (-3.00, 104.80)
- Kalimantan: West (-0.50, 109.50), Central (-2.20, 113.90), South (-3.30, 114.60)

## Method notes

- **Round 1 ENSO index = SOI computed here.** NOAA's site could not be reached from the work environment; the official ONI was added in round 2 as a cross-check. SOI uses the Troup formula on ERA5 monthly Tahiti minus Darwin pressure, 1981–2010 base. Negative = El Niño. It is not the official Bureau of Meteorology SOI series.
- **Singapore metrics are rebuilt from the five regions** for every year, because the `national` field disappears from 2024. PSI = max over regions (NEA's national definition); PM2.5 = mean over the regions reporting that hour.
- Seasonal rain = mean of the three points per island, Aug–Oct, mm/day. A season with any missing day is left blank.

## Known data problems (kept, not filled)

- NEA API has no data before 2016, so the 2015 haze is not in the Singapore series.
- NEA returns "data not found" for 20 days: 2019-08-09, 08-15, 09-06, 09-10, 09-11, 09-14, 09-15, 09-21, 09-25, 09-26, 10-02, 10-17, 10-18; 2021-10-01 to 10-04, 10-25; 2023-10-08, 10-31. Several 2019 gaps fall on peak haze days, so 2019 haze is understated. Some other days have fewer than 24 hourly readings.
- ERA5 values for recent months are preliminary and can be revised. ERA5 tropical rainfall is biased; the 4 mm/day threshold from Field et al. (TRMM-based) is shown for reference only.
- 2026 rain is incomplete (to 10 Oct), so 2026 enters only the "same window" test (1 Aug–10 Oct).
