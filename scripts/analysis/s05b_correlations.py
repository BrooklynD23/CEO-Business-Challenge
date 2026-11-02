"""Step 5b: correlations (requested + own hypotheses), count models, spatial autocorrelation.   [COMPUTED: scripts/analysis/s05b_correlations.py]

Correlation, not cause. Non-significance is not evidence of absence. Spearman with bootstrap CI; Benjamini-Hochberg over ALL tests in the table.
Limited English is an access-need measure only (never a proxy for immigration status).  Race/ethnicity is county-level only in B and is not used here.
Catchment outcome for correlations = fixed 30 km Gaussian E2SFCA (fca_g30_*): it does not use RUCA, so the RUCA-vs-access test is not circular.
"""
import sys, warnings
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd, geopandas as gpd
from scipy import stats
import statsmodels.api as sm, statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from libpysal import weights as lpw
import esda
from config import *
warnings.filterwarnings("ignore")
rng = np.random.default_rng(SEED)

base = pd.read_parquet(PROC / "base_table.parquet").set_index("zcta")
acc = pd.read_parquet(PROC / "access_measures.parquet").set_index("zcta")
cov = pd.read_parquet(PROC / "zcta_covariates.parquet").set_index("zcta")
cl = pd.read_parquet(PROC / "provider_classified.parquet")
df = base[["has_geometry", "county", "in_ie_study", "elig_primary", "is_suppressed", "is_split_zcta", "pw_lat", "pw_lon"]].join(acc.drop(columns=["county", "in_ie_study", "is_split_zcta", "elig_2026_09", "is_suppressed", "ruca", "has_geometry", "min_base_ok"], errors="ignore")).join(cov)
df["zip3"] = df.index.str[:3]
S = df[df.in_ie_study & (df.elig_primary >= 500) & ~df.is_suppressed & df.has_geometry.fillna(False)].copy()
print("analysis sample n =", len(S))

# derived variables
S["log_elig_per_km2"] = np.log(S.elig_per_km2.clip(lower=0.01))
S["log_elig"] = np.log(S.elig_primary)
S["ruca_nonmetro"] = (S.ruca >= 4).astype(int)
S["ruca_class"] = pd.cut(S.ruca, [0, 3, 6, 10], labels=["metro", "small_town", "rural"])
S["inv_income"] = -S.median_hh_income
S["log_income"] = np.log(S.median_hh_income)
vul_vars = ["poverty_rate", "share_hh_no_vehicle", "uninsured_rate", "places_nocheckup", "places_disability", "inv_income"]   # LEP deliberately excluded
Z = (S[vul_vars] - S[vul_vars].mean()) / S[vul_vars].std()
S["vulnerability_index"] = Z.mean(axis=1, skipna=False)
need_vars = ["places_diabetes", "places_chd", "places_nocheckup", "places_depression"]
Zn = (S[need_vars] - S[need_vars].mean()) / S[need_vars].std()
S["chronic_need_index"] = Zn.mean(axis=1, skipna=False)
S["eb_pcp"] = S["eb_per1000_pcp__b"]; S["raw_pcp"] = S["raw_per1000_pcp__b"]
S["fca_pcp"] = S["fca_g30_pcp__b"]; S["fca_mh"] = S["fca_g30_mh__b"]; S["fca_spec"] = S["fca_g30_specialist_all__b"]; S["fca_dental"] = S["fca_g30_dental__b"]
S["fca_card"] = S["fca_g30_cardiology__b"]; S["fca_endo"] = S["fca_g30_endocrinology__b"]; S["fca_obgyn"] = S["fca_g30_obgyn__b"]
S["fca_pcp_g15"] = S["fca_g15_pcp__b"]
S["n_pcp"] = S["n_pcp__b"]; S["n_mh"] = S["n_mh__b"]; S["n_spec"] = S["n_specialist_all__b"]
S["n_pcp_md"] = S["n_pcp_md__b"]; S["n_np"] = S["n_np__b"]
# campus share of PCP (>=100 NPIs at the address)
ie = cl[cl.in_ie].copy()
npa = ie.groupby("addr_key").npi_key.nunique(); ie["npi_at_addr"] = ie.addr_key.map(npa)
pcb = ie[ie.w_pcp__b > 0]
cs = pcb.assign(campus=pcb.npi_at_addr >= 100).groupby("zcta").agg(pc_total=("w_pcp__b", "sum"), pc_campus=("campus", "sum"))
S["campus_share"] = (cs.pc_campus / cs.pc_total).reindex(S.index).fillna(0.0)
# FQHC presence and non-clinic PC supply (catchment excluding clinics is the pcp group: physicians + NPs only)
S["fqhc_sites"] = S.hrsa_sites_permanent
S["fqhc_present"] = (S.fqhc_sites > 0).astype(int)

# ---------------------------------------------------------------- generic test helpers
def rank_w(x): return stats.rankdata(x)
def wcorr(x, y, w):
    xr, yr = rank_w(x), rank_w(y); w = np.asarray(w, float)
    mx, my = np.average(xr, weights=w), np.average(yr, weights=w)
    cov_ = np.average((xr - mx) * (yr - my), weights=w)
    return cov_ / np.sqrt(np.average((xr - mx) ** 2, weights=w) * np.average((yr - my) ** 2, weights=w))
def spearman_row(tid, family, question, xname, yname, data, w="elig_primary", note=""):
    d = data[list(dict.fromkeys([xname, yname, w]))].dropna()
    n = len(d)
    if n < 15 or d[xname].nunique() < 3 or d[yname].nunique() < 3:
        return None
    rho, p = stats.spearmanr(d[xname], d[yname])
    xr, yr = stats.rankdata(d[xname]), stats.rankdata(d[yname])
    idx = rng.integers(0, n, size=(2000, n))
    bs = np.array([np.corrcoef(stats.rankdata(d[xname].values[i]), stats.rankdata(d[yname].values[i]))[0, 1] for i in idx])
    jk = np.array([stats.spearmanr(np.delete(d[xname].values, i), np.delete(d[yname].values, i)).statistic for i in range(n)])
    i_max = int(np.argmax(np.abs(jk - rho)))
    rw = wcorr(d[xname].values, d[yname].values, d[w].values)
    # trimmed: drop top/bottom 5% on x (outlier influence)
    q1, q9 = d[xname].quantile([.05, .95])
    dt = d[(d[xname] >= q1) & (d[xname] <= q9)]
    rt = stats.spearmanr(dt[xname], dt[yname]).statistic if len(dt) > 15 else np.nan
    return dict(id=tid, family=family, question=question, x=xname, y=yname, kind="spearman", n=n, estimate=rho, ci_lo=np.percentile(bs, 2.5), ci_hi=np.percentile(bs, 97.5), p=p,
                weighted_estimate=rw, jackknife_min=jk.min(), jackknife_max=jk.max(), trimmed_5pct_estimate=rt, note=note)
def cliff_row(tid, family, question, gname, yname, data, w="elig_primary", note=""):
    d = data[[gname, yname]].dropna()
    a, b_ = d[d[gname] == 1][yname].values, d[d[gname] == 0][yname].values
    if len(a) < 5 or len(b_) < 5: return None
    u, p = stats.mannwhitneyu(a, b_, alternative="two-sided")
    delta = 2 * u / (len(a) * len(b_)) - 1
    bs = []
    for _ in range(1500):
        aa, bb = rng.choice(a, len(a)), rng.choice(b_, len(b_))
        bs.append(2 * stats.mannwhitneyu(aa, bb).statistic / (len(a) * len(b_)) - 1)
    return dict(id=tid, family=family, question=question, x=gname, y=yname, kind="cliffs_delta(group=1 vs 0)", n=len(d), estimate=delta, ci_lo=np.percentile(bs, 2.5), ci_hi=np.percentile(bs, 97.5), p=p,
                weighted_estimate=np.nan, jackknife_min=np.nan, jackknife_max=np.nan, trimmed_5pct_estimate=np.nan,
                note=f"n_group1={len(a)}, n_group0={len(b_)}, median_group1={np.median(a):.3g}, median_group0={np.median(b_):.3g}. {note}")

R = []
def add(r):
    if r is not None: R.append(r)
REQ, OWN = "requested", "own"
# 1 enrollment density vs supply
for y, lab in [("n_pcp", "PCP count (b)"), ("eb_pcp", "PCP per 1,000 eligibles (EB)"), ("fca_pcp", "PCP catchment (g30)"), ("n_mh", "MH count"), ("fca_mh", "MH catchment")]:
    add(spearman_row(f"R1_{y}", REQ, f"Enrollment density (log eligibles/km2) vs {lab}", "log_elig_per_km2", y, S,
                     note="ratio outcomes share the eligibles denominator, so a negative sign is partly mechanical" if y.startswith("eb") else ""))
    add(spearman_row(f"R1b_{y}", REQ, f"Medi-Cal eligibles (count) vs {lab}", "elig_primary", y, S))
add(spearman_row("R1c_enrolment_rate", REQ, "Medi-Cal enrolment rate (eligibles / ACS population) vs PCP catchment", "elig_per_pop", "fca_pcp", S))
# 2 poverty
for y in ["raw_pcp", "eb_pcp", "fca_pcp", "fca_mh", "fca_spec", "fca_dental"]:
    add(spearman_row(f"R2_{y}", REQ, f"Poverty rate vs {y}", "poverty_rate", y, S))
add(spearman_row("R2_income", REQ, "Median household income vs PCP catchment", "median_hh_income", "fca_pcp", S))
# 3 rurality
for y in ["raw_pcp", "eb_pcp", "fca_pcp", "fca_pcp_g15", "fca_mh", "fca_spec", "fca_dental"]:
    add(spearman_row(f"R3_{y}", REQ, f"Rurality (RUCA 1-10) vs {y}", "ruca", y, S))
# 4 age composition vs specialty supply
add(spearman_row("R4_65_card", REQ, "Share 65+ vs cardiology catchment", "share_65plus", "fca_card", S))
add(spearman_row("R4_65_spec", REQ, "Share 65+ vs all-specialist catchment", "share_65plus", "fca_spec", S))
add(spearman_row("R4_65_pcp", REQ, "Share 65+ vs PCP catchment", "share_65plus", "fca_pcp", S))
add(spearman_row("R4_65_endo", REQ, "Share 65+ vs endocrinology catchment", "share_65plus", "fca_endo", S, note="very few endocrinology records"))
add(spearman_row("R4_fem_obgyn", REQ, "Share women 15-44 vs OB/GYN catchment", "share_female_15_44", "fca_obgyn", S))
add(spearman_row("R4_u18_pcp", REQ, "Share under 18 vs PCP catchment", "share_under18", "fca_pcp", S))
# 5 limited English
for y in ["raw_pcp", "eb_pcp", "fca_pcp", "fca_mh", "fca_spec"]:
    add(spearman_row(f"R5_{y}", REQ, f"Limited-English share (access-need measure) vs {y}", "lep_share_5plus", y, S))
# 6 HPSA vs supply
for y in ["raw_pcp", "fca_pcp"]:
    add(cliff_row(f"R6_{y}", REQ, f"PC-HPSA designated (>=50% of ZCTA land in designated tracts) vs {y}", "hpsa_pc_any", y, S))
    add(spearman_row(f"R6s_{y}", REQ, f"PC-HPSA area share vs {y}", "hpsa_pc_area_share", y, S))
add(cliff_row("R6_mh", REQ, "MH-HPSA designated vs MH catchment", "hpsa_mh_any", "fca_mh", S))
add(cliff_row("R6_dh", REQ, "Dental-HPSA designated vs dental catchment", "hpsa_dh_any", "fca_dental", S))
add(spearman_row("R6_score", REQ, "PC-HPSA max score (designated ZCTAs) vs PCP catchment", "hpsa_pc_max_score", "fca_pcp", S[S.hpsa_pc_any.astype(bool)]))
# 7 vulnerability vs shortage
for y in ["raw_pcp", "eb_pcp", "fca_pcp", "fca_mh", "fca_spec"]:
    add(spearman_row(f"R7_{y}", REQ, f"Vulnerability index (poverty, no vehicle, uninsured, no checkup, disability, low income) vs {y}", "vulnerability_index", y, S))
# --------------- own hypotheses
add(spearman_row("O2_need_pcp", OWN, "Chronic-need index (diabetes, CHD, no checkup, depression) vs PCP catchment", "chronic_need_index", "fca_pcp", S))
add(spearman_row("O2_need_raw", OWN, "Chronic-need index vs raw PCP ratio (EB)", "chronic_need_index", "eb_pcp", S))
add(spearman_row("O2_diab_pcp", OWN, "PLACES diabetes prevalence vs PCP catchment", "places_diabetes", "fca_pcp", S))
add(spearman_row("O2_nocheckup_pcp", OWN, "PLACES no routine checkup vs PCP catchment", "places_nocheckup", "fca_pcp", S))
add(spearman_row("O2_depr_mh", OWN, "PLACES depression vs MH catchment", "places_depression", "fca_mh", S))
add(spearman_row("O3_fqhc_pcp", OWN, "FQHC site count vs private-practice PCP catchment (physicians + NPs)", "fqhc_sites", "fca_pcp", S))
add(cliff_row("O3_fqhc_present", OWN, "FQHC site present vs PCP catchment", "fqhc_present", "fca_pcp", S))
add(spearman_row("O3_fqhc_poverty", OWN, "FQHC site count vs poverty rate", "fqhc_sites", "poverty_rate", S))
add(spearman_row("O4_novehicle_g30", OWN, "Households without a vehicle vs PCP catchment (30 km)", "share_hh_no_vehicle", "fca_pcp", S))
add(spearman_row("O4_novehicle_g15", OWN, "Households without a vehicle vs PCP catchment (15 km)", "share_hh_no_vehicle", "fca_pcp_g15", S))
add(spearman_row("O4_novehicle_raw", OWN, "Households without a vehicle vs raw PCP ratio (EB)", "share_hh_no_vehicle", "eb_pcp", S))
add(spearman_row("O4_lacktrpt", OWN, "PLACES lack of reliable transport vs PCP catchment", "places_lacktrpt", "fca_pcp", S))
add(spearman_row("O9_campus_raw", OWN, "Share of PCPs at 100+-NPI addresses vs raw PCP ratio (EB)", "campus_share", "eb_pcp", S))
add(spearman_row("O9_campus_fca", OWN, "Share of PCPs at 100+-NPI addresses vs PCP catchment", "campus_share", "fca_pcp", S))
add(spearman_row("O10_dental_pcp", OWN, "Dental catchment vs PCP catchment", "fca_dental", "fca_pcp", S))
add(spearman_row("O10_uninsured_pcp", OWN, "Uninsured rate (ACS) vs PCP catchment", "uninsured_rate", "fca_pcp", S))
# Simpson-type: poverty vs raw vs catchment, pooled and within strata
simp = []
for nm, sub in [("pooled", S)] + [(f"RUCA {c}", S[S.ruca_class == c]) for c in ["metro", "small_town", "rural"]] + [(c, S[S.county == c]) for c in ["Riverside", "San Bernardino"]]:
    for y in ["eb_pcp", "fca_pcp"]:
        d = sub[["poverty_rate", y]].dropna()
        if len(d) >= 12:
            r_, p_ = stats.spearmanr(d.poverty_rate, d[y])
            simp.append(dict(stratum=nm, outcome=y, n=len(d), rho=r_, p=p_))
simp = pd.DataFrame(simp); simp.to_csv(TAB / "s05_simpson_poverty_strata.csv", index=False)
# within-county / urban vs desert contrasts (Cliff's delta)
S["desert_east"] = (S.ruca >= 4).astype(int)
add(cliff_row("O6_desert_pcp", OWN, "Non-metro (RUCA>=4) vs metro: PCP catchment", "desert_east", "fca_pcp", S, note="group1 = RUCA>=4"))
add(cliff_row("O6_desert_raw", OWN, "Non-metro (RUCA>=4) vs metro: raw PCP ratio (EB)", "desert_east", "eb_pcp", S))
add(cliff_row("O6_desert_mh", OWN, "Non-metro vs metro: MH catchment", "desert_east", "fca_mh", S))
for cty in ["Riverside", "San Bernardino"]:
    add(cliff_row(f"O6_desert_pcp_{cty[:3]}", OWN, f"Within {cty}: non-metro vs metro, PCP catchment", "desert_east", "fca_pcp", S[S.county == cty]))
S["sb"] = (S.county == "San Bernardino").astype(int)
add(cliff_row("O6_county_pcp", OWN, "San Bernardino vs Riverside: PCP catchment", "sb", "fca_pcp", S, note="group1 = San Bernardino"))
# HPSA misses FFS gaps: detection metrics
d = S[["fca_pcp", "hpsa_pc_any", "hpsa_pc_area_share"]].dropna()
low = d.fca_pcp <= d.fca_pcp.quantile(.25)
det = dict(n=len(d), low_quartile_n=int(low.sum()), hpsa_share_overall=float(d.hpsa_pc_any.mean()), hpsa_share_in_low_quartile=float(d.hpsa_pc_any[low].mean()),
           sensitivity=float(d.hpsa_pc_any[low].mean()), specificity=float((~d.hpsa_pc_any[~low].astype(bool)).mean()),
           low_quartile_not_hpsa=int((low & ~d.hpsa_pc_any.astype(bool)).sum()), hpsa_not_low=int((~low & d.hpsa_pc_any.astype(bool)).sum()))
po = float(((low & d.hpsa_pc_any.astype(bool)).sum() + (~low & ~d.hpsa_pc_any.astype(bool)).sum()) / len(d))
pe = float(d.hpsa_pc_any.mean() * low.mean() + (1 - d.hpsa_pc_any.mean()) * (1 - low.mean()))
det["cohen_kappa"] = (po - pe) / (1 - pe)
# eligibles in low-quartile ZCTAs not covered by a PC-HPSA
det["eligibles_low_quartile_not_hpsa"] = float(S.loc[d.index[low & ~d.hpsa_pc_any.astype(bool)], "elig_primary"].sum())
det["eligibles_low_quartile_total"] = float(S.loc[d.index[low], "elig_primary"].sum())
pd.DataFrame([det]).to_csv(TAB / "s05_hpsa_detection_of_low_ffs_access.csv", index=False)

T = pd.DataFrame(R)
T["p_adj_BH"] = multipletests(T.p.fillna(1), method="fdr_bh")[1]
T["significant_adj_0.05"] = T.p_adj_BH < 0.05
T["n_tests_in_family"] = len(T)
T.to_csv(TAB / "s05_correlation_tests.csv", index=False)
print(T[["id", "n", "estimate", "ci_lo", "ci_hi", "p", "p_adj_BH", "weighted_estimate"]].round(3).to_string())

# ---------------------------------------------------------------- concentration (Lorenz / Gini) on all IE-assigned ZCTAs
def gini(v):
    v = np.sort(np.asarray(v, float)); n = len(v)
    return float((2 * np.sum((np.arange(1, n + 1)) * v) / (n * v.sum())) - (n + 1) / n) if v.sum() > 0 else np.nan
conc = []
sup = pd.read_parquet(PROC / "supply_by_zcta.parquet").set_index("zcta"); sup.columns = [c[2:] if c.startswith("w_") else c for c in sup.columns]
ies = base[base.in_ie_study].index
for g in ["pcp_md", "pcp", "np", "mh", "psychiatrist", "cardiology", "obgyn", "endocrinology", "specialist_all", "dental", "clinic_all"]:
    for d_ in ["b", "e"]:
        col = f"{g}__{d_}"
        if col not in sup.columns: continue
        v = sup.reindex(ies)[col].fillna(0.0).values
        order = np.sort(v)[::-1]; cum = np.cumsum(order) / order.sum()
        k50 = int(np.searchsorted(cum, 0.5) + 1)
        conc.append(dict(group=g, definition=d_, n_zcta=len(v), total=float(v.sum()), gini=gini(v), zcta_holding_half=k50, share_of_zcta_holding_half=k50 / len(v), zcta_with_zero=int((v == 0).sum()),
                         share_zero=float((v == 0).mean()), top_zcta_share=float(order[0] / order.sum())))
# eligible-weighted concentration: do eligibles concentrate as much as supply?
el = base.loc[ies, "elig_primary"].fillna(0).values
conc.append(dict(group="eligibles (denominator)", definition="-", n_zcta=len(el), total=float(el.sum()), gini=gini(el),
                 zcta_holding_half=int(np.searchsorted(np.cumsum(np.sort(el)[::-1]) / el.sum(), .5) + 1), share_of_zcta_holding_half=np.nan, zcta_with_zero=int((el == 0).sum()), share_zero=np.nan, top_zcta_share=np.nan))
pd.DataFrame(conc).to_csv(TAB / "s05_supply_concentration_gini.csv", index=False)
# Lorenz data for figure
lor = {}
for nm, v in [("PCP (b)", sup.reindex(ies)["pcp__b"].fillna(0).values), ("PCP (address-capped e)", sup.reindex(ies)["pcp__e"].fillna(0).values), ("Medi-Cal eligibles", el)]:
    s_ = np.sort(v); lor[nm] = np.concatenate([[0], np.cumsum(s_) / s_.sum()])
pd.to_pickle(lor, PROC / "lorenz_curves.pkl")

# ---------------------------------------------------------------- models: NB counts with offset, OLS on log catchment (robust + cluster), spatial residuals
gdf = gpd.read_file(PROC / "zcta_geometry_region.gpkg").set_index("zcta")
Sg = gdf.loc[S.index].reset_index()
W = lpw.Queen.from_dataframe(Sg, ids=Sg.zcta.tolist(), use_index=False, silence_warnings=True)
W.transform = "r"
def moran(vec, name):
    v = pd.Series(vec, index=S.index).reindex(Sg.zcta).values
    m = esda.Moran(v, W, permutations=999)
    return dict(variable=name, n=len(v), I=float(m.I), E_I=float(m.EI), z_sim=float(m.z_sim), p_sim=float(m.p_sim), islands=int(len(W.islands)))
spatial = []
mod_rows = []
M = S.dropna(subset=["poverty_rate", "lep_share_5plus", "share_65plus", "log_elig_per_km2", "ruca", "uninsured_rate", "share_hh_no_vehicle", "places_diabetes", "median_hh_income"]).copy()
M["ruca_nonmetro"] = (M.ruca >= 4).astype(int)
M["poverty_pct"] = M.poverty_rate * 100; M["lep_pct"] = M.lep_share_5plus * 100; M["age65_pct"] = M.share_65plus * 100; M["novehicle_pct"] = M.share_hh_no_vehicle * 100
M["log_pop_density"] = np.log(M.pop_per_km2.clip(lower=1))
print("model sample", len(M))
formula_rhs = "poverty_pct + lep_pct + age65_pct + novehicle_pct + log_pop_density + ruca_nonmetro + fqhc_present"   # campus_share excluded: it is computed from the outcome count
vif = pd.DataFrame({"variable": formula_rhs.replace(" ", "").split("+")})
Xv = sm.add_constant(M[vif.variable])
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif["VIF"] = [variance_inflation_factor(Xv.values, i + 1) for i in range(len(vif))]
vif.to_csv(TAB / "s05_model_vif.csv", index=False)
for outcome, label in [("n_pcp", "PCP count (b)"), ("n_mh", "MH count (b)"), ("n_spec", "specialist count (b)")]:
    M[outcome] = np.round(M[outcome]).astype(int)
    pois = smf.glm(f"{outcome} ~ {formula_rhs}", data=M, family=sm.families.Poisson(), offset=np.log(M.elig_primary)).fit()
    disp = float(pois.pearson_chi2 / pois.df_resid)
    nb = smf.glm(f"{outcome} ~ {formula_rhs}", data=M, family=sm.families.NegativeBinomial(alpha=1.0), offset=np.log(M.elig_primary)).fit()
    # estimate alpha by moment/MLE
    nbm = smf.negativebinomial(f"{outcome} ~ {formula_rhs}", data=M, offset=np.log(M.elig_primary)).fit(disp=0, maxiter=300)
    alpha = float(nbm.params["alpha"])
    nbr = smf.glm(f"{outcome} ~ {formula_rhs}", data=M, family=sm.families.NegativeBinomial(alpha=max(alpha, 1e-3)), offset=np.log(M.elig_primary)).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(M.zip3)[0]})
    nbh = smf.glm(f"{outcome} ~ {formula_rhs}", data=M, family=sm.families.NegativeBinomial(alpha=max(alpha, 1e-3)), offset=np.log(M.elig_primary)).fit(cov_type="HC1")
    resid = pd.Series(nbr.resid_pearson, index=M.index)
    mi = esda.Moran(resid.reindex(Sg.zcta, fill_value=0).fillna(0).values, W, permutations=999)
    ci = nbr.conf_int()
    for term in nbr.params.index:
        if term == "Intercept": continue
        mod_rows.append(dict(model=f"NB offset(log eligibles): {label}", n=len(M), term=term, rate_ratio=float(np.exp(nbr.params[term])), ci_lo=float(np.exp(ci.loc[term, 0])), ci_hi=float(np.exp(ci.loc[term, 1])),
                             p_cluster_zip3=float(nbr.pvalues[term]), p_HC1=float(nbh.pvalues[term]), poisson_dispersion=disp, nb_alpha=alpha,
                             resid_moran_I=float(mi.I), resid_moran_p=float(mi.p_sim), n_clusters=int(M.zip3.nunique())))
# OLS on log catchment (30 km), unweighted vs weighted, HC3 + cluster, influence
for outcome, label in [("fca_pcp", "PCP catchment (g30)"), ("fca_mh", "MH catchment (g30)"), ("fca_spec", "specialist catchment (g30)")]:
    D_ = M[M[outcome] > 0].copy(); D_["y"] = np.log(D_[outcome])
    f = f"y ~ {formula_rhs}"
    ols = smf.ols(f, data=D_).fit(cov_type="HC3")
    olsc = smf.ols(f, data=D_).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(D_.zip3)[0]})
    wls = smf.wls(f, data=D_, weights=D_.elig_primary).fit(cov_type="HC3")
    infl = smf.ols(f, data=D_).fit().get_influence()
    cook = infl.cooks_distance[0]
    top = np.argsort(cook)[::-1][:3]
    # drop top-3 influence and refit
    keep = np.ones(len(D_), bool); keep[top] = False
    ols_drop = smf.ols(f, data=D_[keep]).fit(cov_type="HC3")
    bp = float(sm.stats.diagnostic.het_breuschpagan(smf.ols(f, data=D_).fit().resid, smf.ols(f, data=D_).fit().model.exog)[1])
    resid = pd.Series(smf.ols(f, data=D_).fit().resid, index=D_.index)
    mi = esda.Moran(resid.reindex(Sg.zcta, fill_value=0).fillna(0).values, W, permutations=999)
    ci = ols.conf_int()
    for term in ols.params.index:
        if term == "Intercept": continue
        mod_rows.append(dict(model=f"OLS log {label}", n=len(D_), term=term, coef=float(ols.params[term]), ci_lo=float(ci.loc[term, 0]), ci_hi=float(ci.loc[term, 1]), pct_effect=float(100 * (np.exp(ols.params[term]) - 1)),
                             p_HC3=float(ols.pvalues[term]), p_cluster_zip3=float(olsc.pvalues[term]), coef_weighted=float(wls.params[term]), p_weighted_HC3=float(wls.pvalues[term]),
                             coef_drop_top3_cook=float(ols_drop.params[term]), r2=float(ols.rsquared), breusch_pagan_p=bp, max_cooks_d=float(cook.max()),
                             resid_moran_I=float(mi.I), resid_moran_p=float(mi.p_sim), n_clusters=int(D_.zip3.nunique())))
mods = pd.DataFrame(mod_rows)
# BH across all model terms (p_cluster_zip3 preferred; falls back to p_HC3)
mods["p_primary"] = mods.p_cluster_zip3
mods["p_adj_BH"] = multipletests(mods.p_primary.fillna(1), method="fdr_bh")[1]
mods.to_csv(TAB / "s05_models.csv", index=False)

# ---------------------------------------------------------------- global Moran's I and LISA
for v, nm in [("eb_pcp", "EB PCP per 1,000 eligibles"), ("fca_pcp", "PCP catchment g30"), ("fca_mh", "MH catchment g30"), ("poverty_rate", "poverty rate"), ("vulnerability_index", "vulnerability index"), ("places_diabetes", "diabetes prevalence")]:
    s_ = S[v].reindex(Sg.zcta)
    vals = s_.fillna(s_.median()).values
    m = esda.Moran(vals, W, permutations=999)
    spatial.append(dict(variable=nm, n=int(s_.notna().sum()), I=float(m.I), E_I=float(m.EI), z_sim=float(m.z_sim), p_sim=float(m.p_sim), n_filled_with_median=int(s_.isna().sum())))
sp = pd.DataFrame(spatial); sp["p_adj_BH"] = multipletests(sp.p_sim, method="fdr_bh")[1]; sp.to_csv(TAB / "s05_global_morans_i.csv", index=False)
lisa_rows = []
for v, nm in [("fca_pcp", "PCP catchment g30"), ("eb_pcp", "EB PCP per 1,000")]:
    s_ = S[v].reindex(Sg.zcta); vals = s_.fillna(s_.median()).values
    li = esda.Moran_Local(vals, W, permutations=999, seed=SEED)
    # BH over local p
    padj = multipletests(li.p_sim, method="fdr_bh")[1]
    q = li.q; lab = np.array(["HH", "LH", "LL", "HL"])[q - 1]
    out = pd.DataFrame({"zcta": Sg.zcta.values, "variable": nm, "quadrant": lab, "I_local": li.Is, "p_sim": li.p_sim, "p_adj_BH": padj})
    out["cluster_0.05_raw"] = np.where(out.p_sim < 0.05, out.quadrant, "ns"); out["cluster_0.10_BH"] = np.where(out.p_adj_BH < 0.10, out.quadrant, "ns")
    out = out.join(S[["county", "elig_primary"]], on="zcta")
    lisa_rows.append(out)
lisa = pd.concat(lisa_rows)
lisa.to_csv(TAB / "s05_lisa_clusters.csv", index=False)
lisa.groupby(["variable", "cluster_0.05_raw"]).size().unstack(fill_value=0).to_csv(TAB / "s05_lisa_cluster_counts.csv")
lisa.groupby(["variable", "cluster_0.10_BH"]).size().unstack(fill_value=0).to_csv(TAB / "s05_lisa_cluster_counts_BH.csv")

# ---------------------------------------------------------------- IE vs neighbours: steepest category gap (whole-region catchment)
rf = pd.read_parquet(PROC / "region_fca.parquet")
rf["is_ie"] = rf.county_fips.isin(IE_FIPS)
cmp_rows = []
for g in ["pcp", "pcp_md", "np", "clinic_all", "mh", "psychiatrist", "cardiology", "obgyn", "endocrinology", "specialist_all", "dental"]:
    for spec in ["g30", "gvar"]:
        col = f"{spec}__{g}__b"
        if col not in rf.columns: continue
        wv = rf.elig_2026_09_imputed
        ie_m = np.average(rf.loc[rf.is_ie, col], weights=wv[rf.is_ie])
        nb_m = np.average(rf.loc[~rf.is_ie, col], weights=wv[~rf.is_ie])
        # LA+OC+SD only
        core = rf.county_fips.isin(["06037", "06059", "06073"])
        core_m = np.average(rf.loc[core, col], weights=wv[core])
        cmp_rows.append(dict(group=g, spec=spec, ie_eligible_weighted_mean=ie_m, neighbour_counties_mean=nb_m, la_oc_sd_mean=core_m, ie_to_neighbour_ratio=ie_m / nb_m, ie_to_la_oc_sd_ratio=ie_m / core_m))
pd.DataFrame(cmp_rows).to_csv(TAB / "s05_ie_vs_neighbour_catchment_by_category.csv", index=False)
S.reset_index().to_parquet(PROC / "analysis_sample.parquet", index=False)
update_checks("correlations", dict(n_sample=len(S), n_model_sample=len(M), n_tests=len(T), n_sig_adj=int(T["significant_adj_0.05"].sum()), hpsa_detection=det,
                                   morans=sp.round(4).to_dict("records")))
print(sp.round(3)); print(pd.DataFrame(conc).round(3).to_string()); print(det)
print(mods[mods.model.str.startswith("NB")].round(3).to_string())
print(mods[mods.model.str.startswith("OLS log PCP")].round(3).to_string())
print(pd.DataFrame(cmp_rows).round(2).to_string()); print(simp.round(3).to_string()); print(vif.round(2))
