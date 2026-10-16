# Confirmatory results under research plan v1 (16 Oct 2026)

Tests exactly as frozen in `research_plan_v1.md`. Numbers from `results/confirmatory_primary.csv`, `confirmatory_robustness.csv`, `confirmatory_diagnostics.csv`, `confirmatory_h3_context.csv`, produced by `src/confirmatory.py`. Key statistics were recomputed with an independent numpy-only script; all matched to 4 decimals.

Reminder: the plan was written after exploratory analysis of the same data, so these are not pre-registered tests (see plan).

## Primary tests

All five reject at α = 0.05 after Holm correction.

| ID | Test | n | Estimate | 95% bootstrap | Holm p | Leave-one-year-out |
|---|---|---|---|---|---|---|
| H1 | ONI Jun–Aug vs Kalimantan Aug–Oct rain (GPCP), Pearson r | 47 | −0.786 | −0.869 to −0.678 | 3.0×10⁻¹⁰ | r from −0.805 to −0.765 |
| H2 | DMI Jun–Aug coefficient on Sumatra rain, ONI held fixed (mm/day per °C) | 47 | −1.674 | −2.705 to −0.611 | 0.0030 | −1.900 to −1.384; worst p 0.014 (drop 1994) |
| H3a | Rain coefficient on log10 Sumatra fires, policy period held fixed | 25 | −0.189 | −0.246 to −0.134 | 1.4×10⁻⁶ | −0.200 to −0.171 |
| H3b | Same, Kalimantan | 25 | −0.160 | −0.195 to −0.137 | 1.9×10⁻⁹ | −0.169 to −0.151 |
| H4 | log10 fires (both islands) vs Singapore Aug–Oct PM2.5, Spearman ρ | 10 | 0.879 | 0.472 to 1.000 | 0.0016 | ρ from 0.833 to 0.917; worst p 0.0053 (drop 2019) |

## What the sizes mean

- **H3:** with the policy period held fixed, each 1 mm/day less Aug–Oct rain goes with about **1.55×** the fire detections in Sumatra and **1.44×** in Kalimantan.
- **Policy period (context, not a primary test):** at the same rain, 2016 onward has about **0.23×** the detections in Sumatra (77% fewer) and **0.53×** in Kalimantan (47% fewer); p < 0.001 and p = 0.002. This matches Sloan et al. (2021, 2022). Model R²: Sumatra 0.821, Kalimantan 0.887.
- **H2:** a 1 °C higher Jun–Aug DMI goes with about 1.7 mm/day less Aug–Oct rain over Sumatra, beyond what El Niño explains.

## Robustness checks (all planned ones except VIIRS)

| ID | Variant | Estimate | p | 95% bootstrap |
|---|---|---|---|---|
| H1 | ERA5 rain | −0.649 | 8.0×10⁻⁷ | −0.762 to −0.522 |
| H2 | ERA5 rain | −1.063 | **0.048** | −1.940 to −0.135 |
| H3a | linear trend instead of policy dummy | −0.208 | 3.0×10⁻⁶ | −0.274 to −0.145 |
| H3a | type-0 fires only | −0.183 | 1.5×10⁻⁶ | −0.243 to −0.124 |
| H3a | ERA5 rain | −0.215 | 5.7×10⁻⁶ | −0.287 to −0.146 |
| H3b | linear trend instead of policy dummy | −0.166 | 1.1×10⁻⁹ | −0.206 to −0.141 |
| H3b | type-0 fires only | −0.159 | 5.4×10⁻¹⁰ | −0.195 to −0.136 |
| H3b | ERA5 rain | −0.153 | 1.1×10⁻⁷ | −0.215 to −0.113 |
| H4 | Pearson instead of Spearman | 0.901 | 3.7×10⁻⁴ | 0.667 to 0.983 |

**Every result keeps its sign and stays below p = 0.05 under every variant.** The weakest is H2 with ERA5 rain (p = 0.048): the IOD effect on Sumatra depends on using the observation-based rain record. This matches round 3, where ERA5 understated the IOD effect.

## Diagnostics and caveats

- Durbin–Watson on residuals (not in the plan, reported for transparency): H2 2.09, H3a **1.44**, H3b 1.99. H3a's value hints at some year-to-year carry-over in Sumatra fires; standard errors there may be somewhat too small. The bootstrap interval and leave-one-out range are less affected and still exclude zero.
- H4 rests on 10 years without 2015. Its bootstrap interval is wide (0.47 to 1.00).
- Bootstrap resamples with a constant column cannot be estimated and were skipped: 1 of 10,000 for one robustness variant (H3b type-0), none elsewhere (`confirmatory_bootstrap_skipped.csv`).
- Correlation and regression on yearly data. "Consistent with" a causal chain, not proof of one.

## What can now be said (headline candidates)

Supported:
1. Jun–Aug El Niño state is a strong early signal for Aug–Oct dryness in Kalimantan (r = −0.79, 47 years).
2. A positive IOD adds extra drying over Sumatra beyond El Niño (observation-based rain).
3. Drier seasons bring more fires on both islands even after allowing for the post-2015 drop in fires.
4. Seasons with more fires are seasons with higher Singapore PM2.5 (ρ = 0.88, 10 years).

Not supported: any statement about whether 2027 will be worse than 2026.
