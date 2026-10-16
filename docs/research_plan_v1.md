# Research plan v1 — FROZEN

Status: approved by Toni and frozen on 16 Oct 2026. Not to be edited; any later change goes in the dated "Deviations" section at the end.

## Honesty statement (will appear in the paper)

This plan was written **after** exploratory rounds 1–4 had already looked at all the data used here, including 2026. It is therefore **not a pre-registration**. Its purpose is to fix the analysis choices and the correction for multiple testing before the robustness checks are run, so results cannot be tuned further. The only data not yet seen are future seasons (2027 onward), which serve as the true out-of-sample test.

## Working title

Climate, fire and Singapore's haze, 2001–2026: a reproducible check with independent observations

## Research questions

1. Does pre-season ocean state (El Niño, IOD) predict Aug–Oct dryness over the main fire regions?
2. Does dryness still predict fire activity once the post-2015 policy regime is accounted for?
3. How closely do fire detections track Singapore's season-average PM2.5?

## Fixed data and definitions

| Item | Choice |
|---|---|
| Season | 1 Aug–31 Oct |
| ENSO index | ONI (NOAA CPC, ERSST v6), Jun–Aug value (known before the season) |
| IOD index | DMI (HadISST1.1), Jun–Aug mean |
| Rain | GPCP v2.3, Aug–Oct mean, nearest 2.5° cell to 3 points per island (cells listed in `gpcp_cells_r3.csv`) |
| Fires | MODIS (FIRMS) standard product, **all detection types**, Aug–Oct count, log10; island boxes as in `analyse_r4.py` |
| Singapore haze | NEA 24-h PM2.5, mean of 5 regions, Aug–Oct season mean |
| Policy regime | dummy = 1 for 2016 onward |
| Years | Rain links 1979–2025; fire links 2001–2025; Singapore link 2016–2025 |

ERA5 rain and computed SOI are used only as sensitivity checks.

## Primary hypotheses and tests (5 tests, Holm-corrected, α = 0.05)

| # | Hypothesis | Test |
|---|---|---|
| H1 | Higher Jun–Aug ONI → lower Aug–Oct rain, Kalimantan | Pearson r, 1979–2025 |
| H2 | Higher Jun–Aug DMI → lower Aug–Oct rain, Sumatra, beyond ONI | Coefficient on DMI in rain ~ ONI + DMI, 1979–2025 |
| H3a | Lower rain → more fires, Sumatra, controlling for policy regime | Coefficient on rain in log fires ~ rain + post2016, 2001–2025 |
| H3b | Same, Kalimantan | as H3a |
| H4 | More fires (both islands) → higher Singapore PM2.5 | Spearman ρ, 2016–2025 |

Note: H1–H2 differ from round 2 in using Jun–Aug indices (genuinely predictive) rather than Aug–Oct (concurrent).

## Robustness checks (all reported, none used to pick results)

1. Leave-one-year-out for every primary test; report the range.
2. Linear detrending instead of the policy dummy (H3).
3. Fires counted as type-0 only (H3), to size the static-source issue.
4. ERA5 rain instead of GPCP (H1–H3).
5. Pearson instead of Spearman (H4); bootstrap 95% intervals throughout.
6. VIIRS (2012 onward) instead of MODIS for H3–H4, if time allows.

## Exploratory (labelled as such, no claims of significance)

- 2019 vs 2023 contrast; 2026 Kalimantan-dominated season.
- Island-level split of H4 (Sumatra vs Kalimantan).
- Smoke transport using ERA5 winds.
- Fire radiative power instead of counts.

## Out-of-sample test

Fit H4 on 2016–2025; record the predicted 2027 Aug–Oct Singapore PM2.5 given 2027 fire counts, before the 2027 PM2.5 is known. Same for a pre-season (Jun–Aug ONI + DMI) prediction of 2027 dryness.

## Out of scope for paper 1

Palm oil prices and land-use economics (paper 2). Health effects. Any statement about causation beyond "consistent with".

## Outputs

- Short paper (6–8 pages, English, IMRaD) plus a Chinese summary.
- Data and code archived with a DOI (Zenodo).
- Later (plan C): extend to a full preprint (EarthArXiv or ESS Open Archive, rules to be checked before submission).

## Deviations

(none yet)
