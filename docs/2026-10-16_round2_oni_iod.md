# Round 2: official ONI cross-check and the Indian Ocean Dipole (16 Oct 2026)

Numbers from `results/correlations_r2.csv`, `regression_r2.csv`, `sg_residual_r2.csv`, `indices_yearly_r2.csv`, produced by `src/analyse_r2.py` in this commit. Index files supplied by Toni (downloaded from NOAA PSL on 16 Oct 2026), saved unchanged in `data/raw/`.

Sign note: SOI is negative in El Niño; ONI and DMI are positive in El Niño / positive IOD. So "more El Niño → less rain" shows as a positive r for SOI and a negative r for ONI.

## 1. Does the round-1 SOI track the official ONI?

Yes, reasonably, but they are not the same index.

- Monthly, 3-month SOI vs ONI, 1950–2025 (n=911): r = −0.788
- Aug–Oct yearly (n=76): r = −0.873

## 2. Round-1 tests redone with ONI

| Test | SOI (round 1) | ONI (round 2) |
|---|---|---|
| Aug–Oct index vs Kalimantan rain, 1950–2025 | r = 0.831 | r = −0.699 (Spearman −0.740) |
| Aug–Oct index vs Sumatra rain | r = 0.721 | r = −0.643 (Spearman −0.639) |
| Jun–Aug index vs Singapore Aug–Oct PM2.5, 2016–2025 | r = −0.833, p = 0.0027 | **r = 0.607, p = 0.063**; Spearman 0.818, p = 0.0038 |
| Jun–Aug index vs PSI>100 days | r = −0.510, p = 0.13 | r = 0.265, p = 0.46 |

- **El Niño → rain survives with the official index** (all p < 0.0001), but is weaker than with SOI.
- **El Niño → Singapore PM2.5 is weaker with ONI**: the Pearson test is no longer significant at 5%; the rank (Spearman) test still is. Round 1's r = −0.833 should not be quoted alone.
- The main year that separates them is 2023: ONI Jun–Aug 1.00 (clear El Niño), SOI Jun–Aug 1.85 (near neutral), Singapore PM2.5 16.08, a middling year.
- Why SOI fits better is not settled. Two candidates: SOI measures the atmosphere, which drives Indonesian rain directly, while ONI measures ocean temperature; **or** SOI and the rain both come from ERA5, and a shared data source can inflate the correlation. Round 2 cannot tell these apart.

## 3. Indian Ocean Dipole

- ONI and DMI overlap: Aug–Oct r = 0.523 (n=76). Positive IOD tends to come with El Niño, so they must be separated.
- DMI alone vs Aug–Oct rain: Sumatra r = −0.549, Kalimantan r = −0.528.
- **DMI with ONI held fixed (partial r):** Sumatra −0.325 (p = 0.0044), Kalimantan −0.266 (p = 0.021). The IOD adds information beyond El Niño, more for Sumatra.
- Regression of rain on ONI + DMI (standardised, 1950–2025):

  | | β ONI | β DMI | R² ONI only | R² ONI + DMI |
  |---|---|---|---|---|
  | Sumatra | −0.490 | −0.292 | 0.414 | 0.476 |
  | Kalimantan | −0.582 | −0.223 | 0.489 | 0.525 |

  The gain is real but modest: about 6 points of R² for Sumatra, 4 for Kalimantan.
- DMI vs Singapore PM2.5, 2016–2025: r = 0.658, p = 0.039 (n=10).

## 4. Does the IOD explain 2019?

Partly, not cleanly.

- Predicting Singapore PM2.5 from Jun–Aug ONI alone, **2019 has the largest positive residual: +6.55 µg/m³** (actual 23.47, predicted 16.92). Its Aug–Oct DMI was 0.76, the second highest of 2016–2025 and second highest since 1950 (after 2023; 1997 was 0.76 to two decimals).
- But **2023 has the highest DMI (0.86) and the most negative residual (−3.87)**. A strong positive IOD did not make 2023 worse than El Niño alone predicts.
- So "2019 was the IOD" is consistent with the data but not shown. Other differences between 2019 and 2023 (where fires burned, wind, fire suppression) are untested.

## 5. 2026

ONI Jun–Aug 1.80, the highest Jun–Aug value in the 1950–2026 file (next: 1997 at 1.48, 2015 at 1.44). Aug–Oct ONI not yet in the file. DMI ends May 2026 (marked preliminary), so the 2026 IOD cannot be tested yet.

## Limits

- Singapore link still rests on 10 years, without 2015.
- 2019 haze understated by 13 missing days.
- 37 tests across rounds 1–2 (18 + 19), no multiple-comparison correction.
- DMI recent values are preliminary.

## Next steps

1. Test whether the SOI advantage is a shared-ERA5 artefact: rerun the rain tests with an independent rainfall record (e.g. CHIRPS or GPCP), if one can be obtained.
2. FIRMS fire counts by island, to see whether 2019 and 2023 differ in where fires burned. Needs the FIRMS key.
3. Palm oil prices (round 3).

## Update (round 3)

With independent GPCP rain, about three-quarters (Sumatra) and half (Kalimantan) of the SOI-over-ONI advantage disappears; it was partly a shared-ERA5 artefact. The El Niño → rain link holds with ONI + GPCP. See `2026-10-16_round3_gpcp.md`.
