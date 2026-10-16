# Round 1: El Niño, Indonesian rain and Singapore haze (16 Oct 2026)

All numbers come from `results/correlations.csv` and `results/yearly.csv` produced by the code in this commit.

## Result

1. **El Niño → Aug–Oct rain (1950–2025, n=76): strong.**
   - Aug–Oct SOI vs Kalimantan rain: Pearson r = 0.831, Spearman 0.848, p < 0.0001
   - Aug–Oct SOI vs Sumatra rain: r = 0.721, Spearman 0.744, p < 0.0001
   - Jun–Aug SOI (two months ahead) vs Aug–Oct rain: Kalimantan r = 0.776, Sumatra r = 0.740
   - Sanity check: the most negative Aug–Oct SOI years are 1982, 2015, 1997, 1994, 2026, all known El Niño years.

2. **El Niño → Singapore haze (2016–2025, n=10): strong for mean PM2.5, weak for unhealthy days.**

   | x | y | Pearson r | p | Spearman ρ | p |
   |---|---|---|---|---|---|
   | Jun–Aug SOI | Aug–Oct mean PM2.5 | −0.833 | 0.0027 | −0.903 | 0.0003 |
   | Jun–Aug SOI | days with PSI > 100 | −0.510 | 0.1317 | −0.649 | 0.0424 |
   | Aug–Oct SOI | Aug–Oct mean PM2.5 | −0.795 | 0.0060 | −0.879 | 0.0008 |
   | Kalimantan rain | Aug–Oct mean PM2.5 | −0.785 | 0.0071 | −0.952 | 0.0000 |
   | Sumatra rain | Aug–Oct mean PM2.5 | −0.806 | 0.0049 | −0.782 | 0.0075 |

   PSI > 100 days are zero in 7 of the 10 years, which is why that measure is weak.

3. **2026 (window 1 Aug–10 Oct, n=11 incl. 2026).** Jun–Aug SOI −16.36, lowest of 2016–2026. Mean PM2.5 35.98 µg/m³ and 24 days with PSI > 100, both far above any other year. With 2026 included, Jun–Aug SOI vs mean PM2.5 gives r = −0.907 (p = 0.0001). This is driven by one extreme point and is not stronger evidence than result 2.

## Limits

- n = 10 (11 with 2026) for the Singapore link. No 2015.
- 2019: SOI near neutral (−0.52 Jun–Aug) yet 6 days with PSI > 100. Possibly the positive Indian Ocean Dipole; not tested. 2019 also has 13 missing days, some on peak haze days.
- SOI is computed from ERA5, not NOAA ONI.
- 18 tests, p-values not corrected for multiple comparisons.
- Correlation, not causation.

## Next steps (in order)

1. Add the IOD (Dipole Mode Index). Needs a file from BoM or NOAA, which the work environment cannot download.
2. Add FIRMS fire counts for Sumatra and Kalimantan: rain → fires → Singapore PM2.5. Needs a FIRMS key.
3. Add palm oil prices: in equally dry years, are there more fires when prices are high? Watch the confounding: El Niño cuts palm output and pushes prices up.
