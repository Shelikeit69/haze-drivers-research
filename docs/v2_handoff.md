# Plan v2 handoff (2 Nov 2026)

This file lists what is done and what is left under `docs/research_plan_v2.md`. The plan is frozen. Read it in full before doing anything; it decides every analysis choice. Any departure from it goes in its "Deviations" section with a date and a reason.

## Done

- Plan v2 frozen (f9c3685).
- Q3 (T3–T6) and robustness 1, 2, 3, 4, 5 and 7: `src/v2_q3.py`, results in `results/v2_q3_results.csv`, note in `docs/2026-11-02_v2_q3_results.md`.
- FIRMS MODIS_SP for 1 Jun – 31 Jul and 1 Nov – 31 Jan, 2002–2025, downloaded with `src/fetch_firms_v2.py` into `data/raw/firms_v2/` (768 files, 195,376 detections; checksums in `data/raw/SHA256SUMS.txt`). These are kept apart from `data/raw/firms/` because `src/analyse_r4.py` reads that whole folder; mixing them would change the v1 results.

## Inputs not in the repository

- Sloan et al. Dryad event data. Download from https://datadryad.org/dataset/doi:10.5061/dryad.msbcc2g1t ("Download full dataset"). Check the SHA256 of the zip against the plan: `0b76226376a13cc8212df0f07041597cd169fba9c7cbdcd8cb6541e80a789e3b`. Unzip outside git into `data/external/sloan_dryad/` (already in `.gitignore`). The inner `Dryad_Version_ofGDB.zip` holds two CSVs: `nfire4_all_spatial_fire_2002_2019_joins_sp_LC.csv` (all detections with event fields, 517 MB) and `..._igs_sp_LC.csv` (ignitions, 114 MB). Read the README .docx first for field definitions.
- The FIRMS key is never written to any file. It is only needed if more FIRMS data is downloaded (VIIRS, robustness 6); pass it as the environment variable FIRMS_MAP_KEY.

## Left to do, in this order

1. **Step 0**: build fire events from FIRMS detections (Aug–Oct in `data/raw/firms/` plus `data/raw/firms_v2/`, years 2002–2019 for validation) with the plan's definitions, and compare with Dryad using the plan's pass rule. Report every comparison number, pass or fail. If it fails, follow the plan's fallback order exactly.
2. **Step 1**: replication models (a) and (b), 2002–2019, 1,000 bootstrap resamples, drop-2015 and drop-2019 runs. No p-values.
3. **T1–T2** over 2002–2025, then the Holm adjustment over T1–T6 (T3–T6 unadjusted p-values are in `results/v2_q3_results.csv`, rows with kind = primary). Robustness 2, 3, 4 and 5 for T1–T2.
4. Robustness 6 (VIIRS) if time allows; robustness 8 (CHIRPS) only if a working download exists.
5. Exploratory items, labelled as exploratory.
6. A results note `docs/<date>_v2_results.md` covering Step 0, Step 1 and T1–T6.

## Small fixes found in review

- `results/v2_q3_results.csv`: the `factor_unit` column is filled for the "context post2016 step" rows, where it does not apply. Fix the labelling in `src/v2_q3.py` and rerun; numbers must not change.
  - Done in `v2-step0`: `factor_unit` is now blank for the context rows. The rerun left every numeric column unchanged.
- Nine files in `data/raw/firms_v2/` are empty (header only), all in wet-season windows (listed by any script that checks `df.empty`). Confirm with the FIRMS API documentation or a re-request that an empty response means no detections, not missing data, and record the answer in the results note.
  - Done in `v2-step0`: the nine files are listed in `results/v2_step0_empty_firms_v2.csv`. The FIRMS missing-data table has no MODIS Terra or Aqua date in those windows, so the files mean zero detections, not missing data. See `docs/2026-11-02_v2_step0_validation.md` section 7.

## Rules

- Every number in a document must come from a script in `src/` and a file in `results/`. No hand-typed or estimated numbers.
- Keep unfavourable results, failed checks and missing data in the write-up. Do not smooth or drop them.
- Do not edit plan v1, v1 results, the paper PDF, or `data/raw/firms/`.
- Seeds fixed in code; scripts runnable as `python src/<name>.py` from the repository root.
- Work on a branch and open a pull request; do not push to main.
