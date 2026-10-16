# Round 4: fires (16 Oct 2026)

Does drought turn into fires, and do fires explain Singapore haze?

Numbers from `results/correlations_r4.csv`, `fire_counts_r4.csv`, `fire_rain_threshold_r4.csv`, `yearly_r4.csv`, produced by `src/analyse_r4.py`; figure `results/fires_r4.png`. Fire data: NASA FIRMS MODIS active-fire detections (Terra + Aqua), downloaded 16 Oct 2026 with Toni's MAP_KEY via `src/fetch_firms.py` (key read from the environment, not stored). 491 raw CSV files saved unchanged in `data/raw/firms/`.

- 2001–2025: MODIS_SP (standard product), 1 Aug–31 Oct.
- 2026: MODIS_NRT (near real time), 1 Aug–15 Oct. **Different processing from SP; treat 2026 as indicative.**
- Island boxes are defined in `analyse_r4.py` (Sumatra box includes Bangka; Peninsular Malaysia, Singapore, Batam/Bintan and most of Sarawak are excluded). Dropped detections ("other"): 178 to 3,570 per year.

## Data decision: count all detections, not only "vegetation fire"

FIRMS marks some detections as "other static land source" (type 2). In 2015, 13,963 of Sumatra's detections were type 2, versus 9 in 2019. They cluster in South Sumatra peatland (around 2.7°S 105.5°E) in Sep–Oct 2015. These look like long-burning peat fires caught by the static-source mask, not industrial sites. Counting only type 0 would undercount the worst peat years, so **the primary count is all detections**. This also matches 2026, whose NRT files have no type column.

## 1. Drought → fires (2001–2025, n=25)

Fire counts are log10-transformed (they span 586 to 62,869).

| | Sumatra | Kalimantan |
|---|---|---|
| GPCP Aug–Oct rain → log fires | r = −0.702 (p = 0.0001) | **r = −0.908** (p < 0.0001) |
| ONI Aug–Oct → log fires | r = 0.577 (p = 0.0025) | r = 0.740 (p < 0.0001) |
| ONI Jun–Aug (2 months ahead) → log fires | r = 0.509 (p = 0.0093) | r = 0.676 (p = 0.0002) |

Below vs above 4 mm/day (GPCP, descriptive only):

| | Dry years (< 4) | Median fires | Wet years (≥ 4) | Median fires |
|---|---|---|---|---|
| Sumatra | 3 (2006, 2015, 2019) | 38,326 | 22 | 8,272 |
| Kalimantan | 4 (2002, 2004, 2006, 2015) | 58,968 | 21 | 9,775 |

Dry years have roughly 4.6× (Sumatra) and 6× (Kalimantan) the median fires of other years. Only 3–4 dry years each, so this is a description, not a test.

## 2. Fires → Singapore PM2.5

| | Aug–Oct, 2016–2025 (n=10) | 1 Aug–10 Oct incl. 2026 (n=11) |
|---|---|---|
| Sumatra log fires | r = 0.915 (p = 0.0002) | r = 0.865 (p = 0.0006) |
| Kalimantan log fires | r = 0.884 (p = 0.0007) | r = 0.891 (p = 0.0002) |
| Both islands | r = 0.901 (p = 0.0004) | — |

**Fire counts track Singapore's PM2.5 more closely than any climate index or rainfall series tested so far.** Sumatra and Kalimantan fires rise and fall together, so with 10 years this cannot say which island matters more.

## 3. Why 2019 was worse than 2023

| | 2019 | 2023 | Ratio |
|---|---|---|---|
| Sumatra fires | 22,720 | 8,394 | 2.71 |
| Kalimantan fires | 32,123 | 15,312 | 2.10 |
| Sumatra GPCP rain, mm/day | 3.23 | 4.16 | |
| Kalimantan GPCP rain, mm/day | 4.19 | 4.51 | |
| Sumatra share of fires | 41.4% | 35.4% | |
| Singapore Aug–Oct PM2.5 | 23.47 | 16.08 | |

2023 had the stronger El Niño, but 2019 had a drier Sumatra (below 4 mm/day) and nearly three times the Sumatra fires. Together with round 3 (the IOD dries Sumatra in particular), a consistent story is: **positive IOD → drier Sumatra → more Sumatra fires → worse Singapore haze**. This chain is consistent with the data but has not been tested as a whole; it rests on two years.

## 4. 2026 so far (NRT, 1 Aug–15 Oct)

- Kalimantan 58,131 detections, Sumatra 16,969. Kalimantan is close to the worst SP years (2015: 62,869 for all of Aug–Oct).
- 1 Aug–10 Oct total: 68,888, versus 83,503 in 2015 and 48,431 in 2019 over the same dates (SP).
- Sumatra is only 22.6% of 2026 fires, yet Singapore PM2.5 is the highest in the record. That does not fit "Sumatra matters most" neatly; smoke transport (wind direction) is the obvious untested factor.

## Limits

- n = 10–11 for the Singapore link; no 2015.
- MODIS Terra and Aqua orbits have drifted in recent years, which can change detection counts; not corrected.
- 2026 NRT is not the same product as SP.
- Fire counts measure detections, not smoke emitted; peat fires emit far more per detection.
- Tests across rounds 1–4: 57 + 11 = 68, no multiple-comparison correction.

## Next steps

1. Wind / smoke transport: which days did air reach Singapore from Sumatra versus Kalimantan? (ERA5 winds are available from Open-Meteo.)
2. Fire radiative power (FRP) instead of counts, as a closer proxy for emissions.
3. Palm oil prices: do equally dry years have more fires when prices are high?
