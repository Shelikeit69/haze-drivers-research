# Post-hoc checks after reviewer feedback (17 and 19 Oct 2026)

Two readers on r/AskStatistics commented on the design: a statistician on 17 October and a second reader on 19 October. The checks below answer their points. None of them was in the frozen plan, so they are reported as post hoc. They do not replace the primary tests, and none of them changes a primary result. The numbers come from `results/posthoc_checks.csv` and `results/posthoc_break_scan.csv`, both produced by `src/posthoc_checks.py`.

## 1. Counts and zeros

No season has zero detections. The smallest season has 586 detections in Sumatra and 1,542 in Kalimantan, so a zero-inflated model is not needed.

## 2. Negative binomial model instead of least squares on log counts

| Island | 1 mm/day less rain, negative binomial | Same, least squares on log10 | Post-2016 factor, negative binomial | Same, least squares |
|---|---|---|---|---|
| Sumatra | ×1.52 (p 1.3e-17) | ×1.55 | ×0.23 | ×0.23 |
| Kalimantan | ×1.44 (p 7.5e-37) | ×1.44 | ×0.55 | ×0.53 |

The count model gives nearly the same effect sizes. Its p-values are much smaller than the least-squares ones, but with 25 years they should not be read as stronger evidence.

## 3. Spurious regression

The rain series and both ocean indices pass the augmented Dickey-Fuller test (unit root rejected, p below 0.001). The KPSS test does not reject stationarity for the El Niño index and the two rain series. It does reject it for the Dipole index (p 0.02), which points to a slow trend. Log fire counts look non-stationary: Sumatra fails the Dickey-Fuller test (p 0.90), and both islands fail KPSS (p 0.04 and 0.03). That fits the break after 2015.

I re-ran the links on year-to-year changes instead of levels:

- El Niño index and Kalimantan rain: r = −0.84 (46 differences, p 4e-13), stronger than the −0.79 in levels.
- Rain and log fires: coefficients of −0.188 in Sumatra and −0.174 in Kalimantan (24 differences, both p below 1e-7), close to −0.189 and −0.160 in levels.
- Fires and Singapore PM2.5: Spearman ρ = 0.90 (9 differences, p 0.001).

The links hold in differences, so shared trends do not explain them.

I also computed Newey-West standard errors with two lags for the rain and fire models. With 25 years they are unreliable, so they are listed only for completeness.

## 4. Points still open

Modelling PM2.5 directly: ten seasons cannot carry a seasonal model with several covariates. A daily model of PM2.5 against lagged fires, rain and wind is the natural next step.

PM2.5 is not the same thing as haze: the seasonal mean also contains local pollution and the effect of humidity. Two options are the excess over a non-haze baseline, or the number of days above a threshold.

## 5. Break year and dependence between years (19 Oct 2026)

Moving the break from 2008 to 2021, one year at a time:

- The rain coefficient barely moves. It stays between −0.177 and −0.225 in Sumatra and between −0.160 and −0.176 in Kalimantan, so the link between drought and fire does not depend on the break year.
- The size of the drop does depend on it. After the break, Sumatra has between 0.21 and 0.51 times the earlier detections, and Kalimantan between 0.53 and 0.82 times. In Kalimantan the step is no longer significant for any break from 2018 onward. The 77% and 47% figures belong to a 2016 break and should be reported that way.
- A 2016 break gives the lowest AIC on both islands, but in Kalimantan a 2012 break is almost as good (−12.03 against −12.17). The year 2016 came from the literature before the final tests, not from this scan. Picking the best year from the scan would overstate the fit.

Step or trend: with a linear trend and the 2016 step in the same model, the trend adds nothing (p 0.73 in Sumatra and 0.72 in Kalimantan), while the step stays significant (p 0.002 and 0.04). Twenty-five years point towards a step, but they cannot rule out a gradual decline.

Unit root with a break: the Zivot-Andrews test with one lag gives p 0.07 for Sumatra (break at 2019) and p 0.05 for Kalimantan (break at 2012). With no lag, the Sumatra test cannot be computed. At this sample size the test is unstable, and I draw no conclusion from it.

Dependence between years: a moving-block bootstrap with blocks of two, three and four years (10,000 resamples each) gives 95% intervals for the rain coefficient of about −0.23 to −0.13 in Sumatra and −0.20 to −0.14 in Kalimantan. These are almost the same as the intervals from resampling single years.

The VIIRS comparison has not been run yet, so drift in the MODIS satellite orbits is still not ruled out.
