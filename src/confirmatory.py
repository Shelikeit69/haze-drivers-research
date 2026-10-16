"""Primary tests and planned robustness checks, exactly as in docs/research_plan_v1.md.

Input: results/yearly_r4.csv (built by rounds 1-4). Run after analyse_r4.py.
Outputs: results/confirmatory_primary.csv, results/confirmatory_robustness.csv

Primary tests (Holm-corrected across the five, alpha 0.05):
  H1  Pearson r, ONI Jun-Aug vs GPCP Aug-Oct rain, Kalimantan, 1979-2025
  H2  OLS GPCP Sumatra rain ~ ONI_JJA + DMI_JJA, 1979-2025; test DMI coefficient
  H3a OLS log10 fires Sumatra ~ GPCP rain + post2016, 2001-2025; test rain coefficient
  H3b same for Kalimantan
  H4  Spearman rho, log10 fires (both islands) vs Singapore Aug-Oct PM2.5, 2016-2025

Robustness (planned): leave-one-year-out; detrending instead of post2016 (H3);
type-0 fires only (H3); ERA5 rain instead of GPCP (H1-H3); Pearson for H4;
bootstrap 95% intervals (10,000 paired resamples, seed 20261016).
VIIRS check (planned "if time allows") is not done here.

Additional diagnostic not in the plan, reported as such: Durbin-Watson on H2/H3 residuals.
"""
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.stattools import durbin_watson

RES = sys.argv[1] if len(sys.argv) > 1 else "results"
y = pd.read_csv(os.path.join(RES, "yearly_r4.csv"), index_col=0)
y["post2016"] = (y.index >= 2016).astype(int)
y["year"] = y.index
for isl in ["sumatra", "kalimantan"]:
    y[f"log_fires_type0_{isl}"] = np.log10(y[f"n_type0_{isl}"])
SEED = 20261016
B = 10000


# ---------- test functions: each returns (statistic, p) on a DataFrame ----------
def pearson(x, yv):
    return lambda d: stats.pearsonr(d[x], d[yv])


def spearman(x, yv):
    return lambda d: tuple(stats.spearmanr(d[x], d[yv]))


def ols_coef(yv, xs, target):
    def f(d):
        m = sm.OLS(d[yv], sm.add_constant(d[xs])).fit()
        return m.params[target], m.pvalues[target]
    return f


def ols_dw(yv, xs):
    def f(d):
        return durbin_watson(sm.OLS(d[yv], sm.add_constant(d[xs])).fit().resid)
    return f


SPECS = {
    # id: (description, years, columns needed, function)
    "H1": ("ONI Jun-Aug vs Kalimantan rain (GPCP), Pearson r", (1979, 2025),
           ["oni_jja", "gpcp_kalimantan_aso"], pearson("oni_jja", "gpcp_kalimantan_aso")),
    "H2": ("DMI Jun-Aug coefficient, Sumatra rain (GPCP) ~ ONI + DMI", (1979, 2025),
           ["gpcp_sumatra_aso", "oni_jja", "dmi_jja"],
           ols_coef("gpcp_sumatra_aso", ["oni_jja", "dmi_jja"], "dmi_jja")),
    "H3a": ("Rain coefficient, log10 fires Sumatra ~ GPCP rain + post2016", (2001, 2025),
            ["log_fires_sumatra", "gpcp_sumatra_aso", "post2016"],
            ols_coef("log_fires_sumatra", ["gpcp_sumatra_aso", "post2016"], "gpcp_sumatra_aso")),
    "H3b": ("Rain coefficient, log10 fires Kalimantan ~ GPCP rain + post2016", (2001, 2025),
            ["log_fires_kalimantan", "gpcp_kalimantan_aso", "post2016"],
            ols_coef("log_fires_kalimantan", ["gpcp_kalimantan_aso", "post2016"], "gpcp_kalimantan_aso")),
    "H4": ("log10 fires (both islands) vs Singapore Aug-Oct PM2.5, Spearman rho", (2016, 2025),
           ["log_fires_both", "sg_pm25_mean"], spearman("log_fires_both", "sg_pm25_mean")),
}

ROBUST = {
    "H1": [("ERA5 rain instead of GPCP", (1979, 2025), ["oni_jja", "rain_kalimantan_aso"],
            pearson("oni_jja", "rain_kalimantan_aso"))],
    "H2": [("ERA5 rain instead of GPCP", (1979, 2025), ["rain_sumatra_aso", "oni_jja", "dmi_jja"],
            ols_coef("rain_sumatra_aso", ["oni_jja", "dmi_jja"], "dmi_jja"))],
    "H3a": [("linear trend instead of post2016", (2001, 2025), ["log_fires_sumatra", "gpcp_sumatra_aso", "year"],
             ols_coef("log_fires_sumatra", ["gpcp_sumatra_aso", "year"], "gpcp_sumatra_aso")),
            ("type-0 fires only", (2001, 2025), ["log_fires_type0_sumatra", "gpcp_sumatra_aso", "post2016"],
             ols_coef("log_fires_type0_sumatra", ["gpcp_sumatra_aso", "post2016"], "gpcp_sumatra_aso")),
            ("ERA5 rain instead of GPCP", (2001, 2025), ["log_fires_sumatra", "rain_sumatra_aso", "post2016"],
             ols_coef("log_fires_sumatra", ["rain_sumatra_aso", "post2016"], "rain_sumatra_aso"))],
    "H3b": [("linear trend instead of post2016", (2001, 2025), ["log_fires_kalimantan", "gpcp_kalimantan_aso", "year"],
             ols_coef("log_fires_kalimantan", ["gpcp_kalimantan_aso", "year"], "gpcp_kalimantan_aso")),
            ("type-0 fires only", (2001, 2025), ["log_fires_type0_kalimantan", "gpcp_kalimantan_aso", "post2016"],
             ols_coef("log_fires_type0_kalimantan", ["gpcp_kalimantan_aso", "post2016"], "gpcp_kalimantan_aso")),
            ("ERA5 rain instead of GPCP", (2001, 2025), ["log_fires_kalimantan", "rain_kalimantan_aso", "post2016"],
             ols_coef("log_fires_kalimantan", ["rain_kalimantan_aso", "post2016"], "rain_kalimantan_aso"))],
    "H4": [("Pearson instead of Spearman", (2016, 2025), ["log_fires_both", "sg_pm25_mean"],
            pearson("log_fires_both", "sg_pm25_mean"))],
}


def data(years, cols):
    return y.loc[years[0]:years[1], cols].dropna()


SKIPPED = {}


def boot_ci(d, f, rng, key):
    """Paired bootstrap. Resamples where any column is constant cannot be estimated
    (e.g. post2016 all 0); they are skipped and counted in SKIPPED[key]."""
    vals = []
    n = len(d)
    skipped = 0
    for _ in range(B):
        s = d.iloc[rng.integers(0, n, n)]
        if (s.nunique() < 2).any():
            skipped += 1
            continue
        v = f(s)[0]
        if not np.isfinite(v):
            skipped += 1
            continue
        vals.append(v)
    SKIPPED[key] = skipped
    return np.percentile(vals, [2.5, 97.5])


def loo(d, f):
    out = []
    for yr in d.index:
        st, p = f(d.drop(index=yr))
        out.append((yr, st, p))
    o = pd.DataFrame(out, columns=["dropped", "stat", "p"])
    worst = o.loc[o["p"].idxmax()]
    return o["stat"].min(), o["stat"].max(), worst["p"], int(worst["dropped"])


rng = np.random.default_rng(SEED)
prim = []
for hid, (desc, yrs, cols, f) in SPECS.items():
    d = data(yrs, cols)
    st, p = f(d)
    lo, hi = boot_ci(d, f, rng, hid)
    lmin, lmax, lp, ly = loo(d, f)
    prim.append({"id": hid, "test": desc, "n": len(d), "years": f"{d.index.min()}-{d.index.max()}",
                 "stat": round(float(st), 4), "p_raw": float(p),
                 "boot95_low": round(float(lo), 4), "boot95_high": round(float(hi), 4),
                 "loo_stat_min": round(float(lmin), 4), "loo_stat_max": round(float(lmax), 4),
                 "loo_max_p": float(lp), "loo_max_p_dropped": ly})
prim = pd.DataFrame(prim)
rej, p_holm, _, _ = multipletests(prim["p_raw"], alpha=0.05, method="holm")
prim["p_holm"] = p_holm
prim["significant_holm_0.05"] = rej
prim.to_csv(os.path.join(RES, "confirmatory_primary.csv"), index=False)

rob = []
for hid, items in ROBUST.items():
    for desc, yrs, cols, f in items:
        d = data(yrs, cols)
        st, p = f(d)
        lo, hi = boot_ci(d, f, rng, f"{hid} | {desc}")
        rob.append({"id": hid, "variant": desc, "n": len(d), "stat": round(float(st), 4), "p": float(p),
                    "boot95_low": round(float(lo), 4), "boot95_high": round(float(hi), 4)})
# Additional diagnostic (not in plan)
diag = []
for hid, yv, xs, yrs in [("H2", "gpcp_sumatra_aso", ["oni_jja", "dmi_jja"], (1979, 2025)),
                         ("H3a", "log_fires_sumatra", ["gpcp_sumatra_aso", "post2016"], (2001, 2025)),
                         ("H3b", "log_fires_kalimantan", ["gpcp_kalimantan_aso", "post2016"], (2001, 2025))]:
    d = data(yrs, [yv] + xs)
    diag.append({"id": hid, "durbin_watson": round(float(ols_dw(yv, xs)(d)), 3)})
rob = pd.DataFrame(rob)
rob.to_csv(os.path.join(RES, "confirmatory_robustness.csv"), index=False)
pd.DataFrame(diag).to_csv(os.path.join(RES, "confirmatory_diagnostics.csv"), index=False)

# Post2016 coefficients (context for H3; reported, not tested)
ctx = []
for isl in ["sumatra", "kalimantan"]:
    d = data((2001, 2025), [f"log_fires_{isl}", f"gpcp_{isl}_aso", "post2016"])
    m = sm.OLS(d[f"log_fires_{isl}"], sm.add_constant(d[[f"gpcp_{isl}_aso", "post2016"]])).fit()
    ctx.append({"island": isl, "coef_rain": round(m.params[f"gpcp_{isl}_aso"], 4),
                "coef_post2016": round(m.params["post2016"], 4), "p_post2016": round(m.pvalues["post2016"], 4),
                "r2": round(m.rsquared, 3)})
pd.DataFrame(ctx).to_csv(os.path.join(RES, "confirmatory_h3_context.csv"), index=False)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 30)
print(prim.to_string(index=False))
print()
print(rob.to_string(index=False))
print()
print(pd.DataFrame(diag).to_string(index=False))
print()
print(pd.DataFrame(ctx).to_string(index=False))
pd.Series(SKIPPED, name="skipped_resamples").to_csv(os.path.join(RES, "confirmatory_bootstrap_skipped.csv"))
print()
print("skipped bootstrap resamples:", SKIPPED)
