"""Post-hoc checks after reviewer feedback (r/AskStatistics, 17 Oct 2026).
NOT part of the frozen plan in docs/research_plan_v1.md. Reported as extra robustness only.

1. Zero counts in seasonal fire detections.
2. Negative binomial GLM (log link) instead of OLS on log10 counts (H3).
3. First differences instead of levels (H1, H3, H4) to guard against spurious regression.
4. ADF and KPSS stationarity tests on each series.
5. HAC (Newey-West, 2 lags) standard errors for H3 OLS.
6. (second reviewer, 19 Oct) Break-year scan 2008-2021, step vs linear trend, Zivot-Andrews
   unit-root test with one break, moving-block bootstrap (block 2-4 years) for the H3 rain coefficient.

Also writes results/posthoc_break_scan.csv

Output: results/posthoc_checks.csv
"""
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews

warnings.filterwarnings("ignore")
RES = sys.argv[1] if len(sys.argv) > 1 else "results"
y = pd.read_csv(os.path.join(RES, "yearly_r4.csv"), index_col=0)
y["post2016"] = (y.index >= 2016).astype(int)
d = y.loc[2001:2025]
rows = []


def add(check, item, stat, p=np.nan, n=np.nan, note=""):
    rows.append({"check": check, "item": item, "stat": round(float(stat), 4),
                 "p": float(p), "n": n, "note": note})


for isl in ["sumatra", "kalimantan"]:
    n = d[f"n_all_{isl}"]
    add("zero_counts", isl, (n == 0).sum(), n=len(n), note=f"min {int(n.min())}, max {int(n.max())}")
    X = sm.add_constant(d[[f"gpcp_{isl}_aso", "post2016"]])
    nb = sm.NegativeBinomial(n, X).fit(disp=0)
    b = nb.params[f"gpcp_{isl}_aso"]
    add("negbin_rain_coef", isl, b, nb.pvalues[f"gpcp_{isl}_aso"], len(n),
        f"x{np.exp(-b):.3f} fires per 1 mm/day less rain; post2016 x{np.exp(nb.params['post2016']):.3f}")
    ols = sm.OLS(np.log10(n), X).fit()
    add("ols_log10_rain_coef", isl, ols.params[f"gpcp_{isl}_aso"], ols.pvalues[f"gpcp_{isl}_aso"], len(n),
        f"x{10 ** (-ols.params[f'gpcp_{isl}_aso']):.3f} per 1 mm/day less rain")
    hac = sm.OLS(np.log10(n), X).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
    add("ols_hac2_rain_coef", isl, hac.params[f"gpcp_{isl}_aso"], hac.pvalues[f"gpcp_{isl}_aso"], len(n))
    dd = d[[f"log_fires_{isl}", f"gpcp_{isl}_aso", "post2016"]].diff().dropna()
    fd = sm.OLS(dd[f"log_fires_{isl}"], sm.add_constant(dd[[f"gpcp_{isl}_aso", "post2016"]])).fit()
    add("first_diff_rain_coef", isl, fd.params[f"gpcp_{isl}_aso"], fd.pvalues[f"gpcp_{isl}_aso"], len(dd))

a = y.loc[1979:2025, ["oni_jja", "gpcp_kalimantan_aso"]].dropna().diff().dropna()
r = stats.pearsonr(a.iloc[:, 0], a.iloc[:, 1])
add("first_diff_H1_pearson", "oni vs kalimantan rain", r[0], r[1], len(a))
b4 = y.loc[2016:2025, ["log_fires_both", "sg_pm25_mean"]].dropna().diff().dropna()
s = stats.spearmanr(b4.iloc[:, 0], b4.iloc[:, 1])
add("first_diff_H4_spearman", "fires vs sg pm25", s[0], s[1], len(b4))

series = {"oni_jja": y.loc[1979:2025, "oni_jja"], "dmi_jja": y.loc[1979:2025, "dmi_jja"],
          "gpcp_sumatra_aso": y.loc[1979:2025, "gpcp_sumatra_aso"],
          "gpcp_kalimantan_aso": y.loc[1979:2025, "gpcp_kalimantan_aso"],
          "log_fires_sumatra": d["log_fires_sumatra"], "log_fires_kalimantan": d["log_fires_kalimantan"]}
for k, v in series.items():
    v = v.dropna()
    add("adf (H0 unit root)", k, adfuller(v, autolag="AIC")[0], adfuller(v, autolag="AIC")[1], len(v))
    add("kpss (H0 stationary; p capped 0.01-0.10)", k, kpss(v, nlags="auto")[0], kpss(v, nlags="auto")[1], len(v))

scan = []
for isl in ["sumatra", "kalimantan"]:
    yv = d[f"log_fires_{isl}"]
    r = d[f"gpcp_{isl}_aso"]
    for k in range(2008, 2022):
        X = sm.add_constant(pd.DataFrame({"rain": r, "post": (d.index >= k).astype(int)}))
        m = sm.OLS(yv, X).fit()
        scan.append({"island": isl, "break_year": k, "aic": round(m.aic, 2), "rain_coef": round(m.params["rain"], 4),
                     "step_factor": round(10 ** m.params["post"], 3), "p_step": m.pvalues["post"]})
    Xb = sm.add_constant(pd.DataFrame({"rain": r, "t": d.index - 2001, "post": (d.index >= 2016).astype(int)}))
    mb = sm.OLS(yv, Xb).fit()
    add("trend_plus_step: p_trend", isl, mb.params["t"], mb.pvalues["t"], len(yv))
    add("trend_plus_step: p_step", isl, mb.params["post"], mb.pvalues["post"], len(yv))
    za = zivot_andrews(yv.values, regression="c", maxlag=1, autolag=None)
    add("zivot_andrews (maxlag 1)", isl, za[0], za[1], len(yv), f"break year {2001 + za[4]}; unstable at n=25")
    rng = np.random.default_rng(20261016)
    n_ = len(d)
    X = sm.add_constant(pd.DataFrame({"rain": r, "post": (d.index >= 2016).astype(int)}))
    for L in [2, 3, 4]:
        vals, skip = [], 0
        for _ in range(10000):
            starts = rng.integers(0, n_ - L + 1, int(np.ceil(n_ / L)))
            idx = np.concatenate([np.arange(s0, s0 + L) for s0 in starts])[:n_]
            Xs = X.iloc[idx]
            if Xs["post"].nunique() < 2:
                skip += 1
                continue
            vals.append(np.linalg.lstsq(Xs.values, yv.iloc[idx].values, rcond=None)[0][1])
        lo, hi = np.percentile(vals, [2.5, 97.5])
        add(f"block_bootstrap_L{L}_rain_coef_CI", isl, lo, np.nan, len(vals), f"95% CI {lo:.3f} to {hi:.3f}; skipped {skip}")
pd.DataFrame(scan).to_csv(os.path.join(RES, "posthoc_break_scan.csv"), index=False)

out = pd.DataFrame(rows)
out.to_csv(os.path.join(RES, "posthoc_checks.csv"), index=False)
pd.set_option("display.width", 200)
print(out.to_string(index=False))
