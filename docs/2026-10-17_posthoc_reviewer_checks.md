# Post-hoc checks after reviewer feedback (17 Oct 2026)

A statistician (PhD, r/AskStatistics) raised four points on the design. These checks respond to them. They are **post hoc**, outside the frozen plan, and do not replace the primary tests. Numbers from `results/posthoc_checks.csv`, produced by `src/posthoc_checks.py`.

## 1. Counts and zeros

No season has zero detections. Minimum is 586 (Sumatra) and 1,542 (Kalimantan), so a zero-inflated model is not needed.

## 2. Negative binomial instead of OLS on log10 counts

| Island | 1 mm/day less rain (NB) | Same (OLS log10) | Post-2016 factor (NB) | Same (OLS) |
|---|---|---|---|---|
| Sumatra | ×1.52 (p 1.3e-17) | ×1.55 | ×0.23 | ×0.23 |
| Kalimantan | ×1.44 (p 7.5e-37) | ×1.44 | ×0.55 | ×0.53 |

The count model gives nearly the same effect sizes. NB p-values are much smaller than OLS ones; with n = 25 they should not be read as more convincing.

## 3. Spurious regression

Rain, ONI and DMI pass ADF (unit root rejected, p < 0.001). KPSS does not reject stationarity for ONI and both rain series, but does for DMI (p 0.02), which suggests a slow trend. Log fire counts look non-stationary: Sumatra fails ADF (p 0.90), and both islands fail KPSS (p 0.04 and 0.03), consistent with the post-2015 break.

Re-running in first differences (year-to-year changes):

- H1: r = −0.84 (n = 46, p 4e-13), stronger than in levels (−0.79).
- H3: rain coefficient −0.188 Sumatra, −0.174 Kalimantan (n = 24, both p < 1e-7), close to levels (−0.189, −0.160).
- H4: Spearman ρ = 0.90 (n = 9, p 0.001).

The links survive differencing, so they are not driven by shared trends.

HAC (Newey–West, 2 lags) standard errors were also computed for H3. With n = 25 they are unreliable and are listed only for completeness.

## 4. Points not yet addressed

- **Model PM2.5 directly.** With ten seasons, a seasonal PM2.5 model cannot take many covariates. A daily model (PM2.5 against lagged fires, rain and wind) is the natural next step.
- **PM2.5 is not the same as haze.** The seasonal mean includes local pollution and humidity effects. Options: excess over a non-haze baseline, or days above a threshold.

## 5. Second reviewer (19 Oct 2026): break year and dependence

Numbers from `results/posthoc_checks.csv` and `results/posthoc_break_scan.csv`.

**Break year.** Moving the step from 2008 to 2021 one year at a time:

- The rain coefficient barely moves: Sumatra −0.177 to −0.225, Kalimantan −0.160 to −0.176. The drought-fire link does not depend on the break year.
- The size of the drop does: Sumatra ×0.21 to ×0.51, Kalimantan ×0.53 to ×0.82, and in Kalimantan the step stops being significant for breaks from 2018 on. **The 77% and 47% figures are specific to a 2016 break and should be reported as such.**
- 2016 gives the lowest AIC on both islands, but Kalimantan 2012 is close (AIC −12.03 against −12.17). The 2016 choice came from the literature before the final tests, not from this scan; picking the best year from the scan would overstate the fit.

**Step or trend.** With both a linear trend and the 2016 step in the model, the trend adds nothing (p 0.73 Sumatra, 0.72 Kalimantan) while the step stays (p 0.002, 0.04). With 25 years this leans towards a step but does not rule out a gradual change.

**Unit root with a break.** Zivot–Andrews with one lag gives p 0.07 (Sumatra, break 2019) and 0.05 (Kalimantan, break 2012). With no lag the Sumatra test fails to compute. At n = 25 the test is unstable; no conclusion drawn.

**Dependence-aware bootstrap.** A moving-block bootstrap (blocks of 2, 3 and 4 years, 10,000 resamples) gives 95% intervals for the rain coefficient of about −0.23 to −0.13 (Sumatra) and −0.20 to −0.14 (Kalimantan), almost the same as the year-by-year bootstrap.

**VIIRS.** Still not run, so MODIS orbital drift is not ruled out.
