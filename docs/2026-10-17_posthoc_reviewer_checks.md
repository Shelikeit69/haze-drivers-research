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
