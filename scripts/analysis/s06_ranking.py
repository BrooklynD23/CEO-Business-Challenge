"""Step 6: preliminary gap ranking, rank stability (weight sweep, status-blind Dirichlet demand perturbation, random dormancy thinning,
supply-definition choice) and the unit-of-analysis test.   [COMPUTED: scripts/analysis/s06_ranking.py]

TITLE OF THE RANKING: "general FFS supply shortfall among all Medi-Cal eligibles" - it is NOT a map of where transitioning members lose access.
Perturbation: ZCTA-level shares of a regional mover total are drawn from a Dirichlet around the uniform (eligibles-proportional) share. The draws do not use
any covariate, race, language or status variable; they only ask whether the uniform-share assumption changes the ranking.
"""
import sys, warnings
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd, geopandas as gpd
from scipy import stats, sparse
from scipy.spatial import cKDTree
from sklearn.decomposition import PCA
from config import *
warnings.filterwarnings("ignore")
rng = np.random.default_rng(SEED)

S = pd.read_parquet(PROC / "analysis_sample.parquet").set_index("zcta")
dem = pd.read_parquet(PROC / "zcta_demand_region.parquet")
pts = pd.read_parquet(PROC / "supply_points_region.parquet")
ruca = pd.read_csv(RAW / "X_usda_ruca_zip/2020-rural-urban-commuting-area-codes-zip-codes.csv", dtype=str).rename(columns={"ZIPCode": "zcta", "PrimaryRUCA": "ruca"})
ruca["ruca"] = pd.to_numeric(ruca.ruca, errors="coerce")
dem = dem.merge(ruca[["zcta", "ruca"]].drop_duplicates("zcta"), on="zcta", how="left")
dem["d0"] = np.where(dem.ruca.fillna(4) <= 3, 15e3, np.where(dem.ruca.fillna(4) <= 6, 30e3, 60e3))
con = duck()
B2 = RAW / "B_delivery_plan/t2_eligibility_by_delivery_system_plan_201001_oct2026.csv"
b = con.execute(f"""select County as county, "Health Delivery System" as sys, {num('"Total Eligibles"')} as n from read_csv('{B2}', all_varchar=true, header=true)
                    where "Month of Eligibility"='2026-09' and County<>'STATEWIDE'""").df()
b["n"] = b.n.astype("float64")
bc = b.groupby(["county", "sys"]).n.sum().unstack().fillna(0.0)
cty = gpd.read_file(f"zip://{RAW / 'X_tiger_county_2020' / 'cb_2020_us_county_500k.zip'}")
fips2name = cty[cty.STATEFP == "06"].set_index("GEOID").NAME.to_dict()
dem["cname"] = dem.county_fips.map(fips2name)

D = dem[dem.is_ca_demand & (dem.elig_2026_09_imputed > 0)].reset_index(drop=True)
D["ffs_c"] = D.cname.map(bc["Fee-for-Service"]); D["mc_c"] = D.cname.map(bc["Managed Care"])
D = D.dropna(subset=["ffs_c", "mc_c"]).reset_index(drop=True)
E_i = D.elig_2026_09_imputed.values.astype(float)
cnames = D.cname.values
county_idx = {c: np.where(cnames == c)[0] for c in np.unique(cnames)}
S_SHARE = 0.10          # share of managed-care members who move, applied uniformly across counties for this exercise (IEHP's stated ~10%)
def demand_baseline():
    d = np.zeros(len(D))
    for c, ix in county_idx.items():
        pi = E_i[ix] / E_i[ix].sum()
        d[ix] = (D.ffs_c.values[ix][0] + S_SHARE * D.mc_c.values[ix][0]) * pi
    return d
def demand_dirichlet(alpha):
    d = np.zeros(len(D))
    for c, ix in county_idx.items():
        pi = E_i[ix] / E_i[ix].sum()
        v = rng.dirichlet(np.maximum(alpha * pi, 1e-6))
        d[ix] = D.ffs_c.values[ix][0] * pi + S_SHARE * D.mc_c.values[ix][0] * v
    return d
sx = pts[["lx", "ly"]].values
rec = cKDTree(D[["x", "y"]].values).sparse_distance_matrix(cKDTree(sx), 60_000.0, output_type="ndarray")
I, J, dist = rec["i"].astype(np.int64), rec["j"].astype(np.int64), rec["v"].astype(float)
d0 = D.d0.values[I]
w = np.where(dist <= d0, (np.exp(-0.5 * (dist / d0) ** 2) - np.exp(-0.5)) / (1 - np.exp(-0.5)), 0.0)
k = w > 0
Wm = sparse.csr_matrix((w[k], (I[k], J[k])), shape=(len(D), len(pts)))
COMP = {"PCP": "pcp__b", "MH": "mh__b", "SPEC": "specialist_all__b", "DENTAL": "dental__b"}
Smat = pts[[f"w_{v}" for v in COMP.values()]].values.astype(float)
def acc(dw, Sm=Smat):
    den = Wm.T @ dw
    R = np.divide(Sm, den[:, None], out=np.zeros_like(Sm), where=den[:, None] > 0)
    return (Wm @ R) * 1000.0
idx_S = pd.Index(D.zcta).get_indexer(S.index)
assert (idx_S >= 0).all(), "analysis ZCTAs missing from demand set"
base_dw = demand_baseline()
A0 = acc(base_dw)[idx_S]                                   # (n_S, 4)  baseline accessibility under existing-FFS + 10% movers (uniform)
n = len(S)
pct = lambda x: stats.rankdata(x) / len(x)

# ---- components (percentile of shortfall, higher = worse); NEED = percentile mean of chronic need, no vehicle, poverty (LEP deliberately not used)
def shortfall(A): return 1 - np.column_stack([pct(A[:, j]) for j in range(A.shape[1])])
SF0 = shortfall(A0)
need_df = pd.DataFrame({"need": S.chronic_need_index, "novehicle": S.share_hh_no_vehicle, "poverty": S.poverty_rate})
need_pct = need_df.apply(lambda c: pct(c.fillna(c.median()).values)).mean(axis=1).values
need_pct = pct(need_pct)
X0 = np.column_stack([SF0, need_pct])                      # PCP, MH, SPEC, DENTAL, NEED
NAMES = list(COMP) + ["NEED"]
W_EQ = np.full(5, 0.2)
W_EV = np.array([0.35, 0.20, 0.15, 0.05, 0.25])
pca = PCA(n_components=1).fit((X0 - X0.mean(0)) / X0.std(0))
load = pca.components_[0]
if load.sum() < 0: load = -load
W_PCA = np.abs(load) / np.abs(load).sum()
schemes = {"equal": W_EQ, "evidence": W_EV, "pca": W_PCA}
comp = {nme: X0 @ wv for nme, wv in schemes.items()}
rank = {nme: stats.rankdata(-v, method="average") for nme, v in comp.items()}      # rank 1 = largest shortfall
supply_only = {nme: (X0[:, :4] @ (wv[:4] / wv[:4].sum())) for nme, wv in schemes.items()}
# exposure-weighted (shortfall x eligibles)
expo = {nme: v * S.elig_primary.values for nme, v in comp.items()}

# ---- weight sweep
NSW = 2000
Wd = rng.dirichlet(np.ones(5), size=NSW)
comp_sw = X0 @ Wd.T                                                 # n x NSW
rank_sw = np.apply_along_axis(lambda v: stats.rankdata(-v), 0, comp_sw)
top10 = int(round(0.1 * n))
in_top_sw = (rank_sw <= top10)
freq_top_sw = in_top_sw.mean(axis=1)
rank_med = np.median(rank_sw, axis=1); rank_p5 = np.percentile(rank_sw, 5, axis=1); rank_p95 = np.percentile(rank_sw, 95, axis=1)
# Spearman between each sweep ranking and the 3 named schemes
sw_corr = [stats.spearmanr(rank_sw[:, j], rank["equal"]).statistic for j in range(0, NSW, 10)]

# ---- demand perturbation (status-blind Dirichlet)
ALPHAS = [10_000, 2_000, 1_000, 300, 100, 30]
NDR = 150
pert_rows, top_freq_pert = [], {}
agg_levels = {"ZCTA": S.index.values, "4-digit ZIP prefix": np.array([z[:4] for z in S.index]), "ZIP3": np.array([z[:3] for z in S.index]), "county x RUCA class": np.array([f"{c}|{'metro' if r <= 3 else 'non-metro'}" for c, r in zip(S.county, S.ruca)])}
def agg_rank(vec, labels):
    g = pd.DataFrame({"u": labels, "v": vec, "w": S.elig_primary.values}).groupby("u").apply(lambda d: np.average(d.v, weights=d.w))
    return g
base_agg = {lv: agg_rank(comp["equal"], labs) for lv, labs in agg_levels.items()}
base_agg_ev = {lv: agg_rank(comp["evidence"], labs) for lv, labs in agg_levels.items()}
for alpha in ALPHAS:
    cvs, rho_eq, rho_ev, cnt_top_eq, cnt_top_ev = [], {lv: [] for lv in agg_levels}, [], np.zeros(n), np.zeros(n)
    top_q_ret = {lv: [] for lv in agg_levels}
    for r in range(NDR):
        dw = demand_dirichlet(alpha)
        # realised CV of the ZCTA transition share relative to the uniform share
        mult = []
        for c, ix in county_idx.items():
            pi = E_i[ix] / E_i[ix].sum(); mv = dw[ix] - D.ffs_c.values[ix][0] * pi
            mult.append((mv / (S_SHARE * D.mc_c.values[ix][0])) / pi)
        m_ = np.concatenate(mult); cvs.append(np.std(m_[np.isfinite(m_)]) / np.mean(m_[np.isfinite(m_)]))
        A = acc(dw)[idx_S]
        X = np.column_stack([shortfall(A), need_pct])
        ce = X @ W_EQ; cv_ = X @ W_EV
        r_e = stats.rankdata(-ce); r_v = stats.rankdata(-cv_)
        rho_eq["ZCTA"].append(stats.spearmanr(r_e, rank["equal"]).statistic)
        rho_ev.append(stats.spearmanr(r_v, rank["evidence"]).statistic)
        cnt_top_eq += (r_e <= top10); cnt_top_ev += (r_v <= top10)
        for lv, labs in agg_levels.items():
            if lv == "ZCTA":
                top_q_ret[lv].append(len(set(np.where(r_e <= max(1, n // 4))[0]) & set(np.where(rank["equal"] <= max(1, n // 4))[0])) / max(1, n // 4)); continue
            ag = agg_rank(ce, labs)
            rho_eq[lv].append(stats.spearmanr(ag.reindex(base_agg[lv].index).values, base_agg[lv].values).statistic)
            kq = max(1, int(round(len(ag) / 4)))
            top_q_ret[lv].append(len(set(ag.nlargest(kq).index) & set(base_agg[lv].nlargest(kq).index)) / kq)
    top_freq_pert[alpha] = cnt_top_eq / NDR
    row = dict(alpha=alpha, realised_cv_of_zcta_transition_share=float(np.mean(cvs)), draws=NDR)
    for lv in agg_levels:
        row[f"mean_spearman_vs_baseline_equal_{lv}"] = float(np.mean(rho_eq[lv]))
        row[f"p5_spearman_equal_{lv}"] = float(np.percentile(rho_eq[lv], 5))
        row[f"top_quartile_retention_{lv}"] = float(np.mean(top_q_ret[lv]))
    row["mean_spearman_vs_baseline_evidence_ZCTA"] = float(np.mean(rho_ev))
    row["share_baseline_top_decile_retained_equal"] = float(np.mean(top_freq_pert[alpha][rank["equal"] <= top10]))
    row["share_baseline_top_decile_retained_evidence"] = float(np.mean((cnt_top_ev / NDR)[rank["evidence"] <= top10]))
    pert_rows.append(row)
pert = pd.DataFrame(pert_rows); pert.to_csv(TAB / "s06_demand_perturbation_stability.csv", index=False)

# ---- spatially coherent (but status-blind) random unevenness: a smoothed Gaussian random field multiplies the uniform share, so whole neighbourhoods are
# over- or under-represented together. This is the harder test of the uniform assumption; the field is random, uses no covariate and locates nobody.
tD = cKDTree(D[["x", "y"]].values)
def demand_field(sigma, h_km):
    h = h_km * 1000.0
    pr = tD.sparse_distance_matrix(tD, 3 * h, output_type="coo_matrix")
    Kw = sparse.csr_matrix((np.exp(-0.5 * (pr.data / h) ** 2), (pr.row, pr.col)), shape=(len(D), len(D)))
    Kw = Kw + sparse.identity(len(D))                  # self weight (zero distance entries are not stored)
    norm = np.sqrt(np.asarray(Kw.multiply(Kw).sum(axis=1)).ravel())
    z = (Kw @ rng.standard_normal(len(D))) / norm
    mult = np.exp(sigma * z - sigma ** 2 / 2)
    d = np.zeros(len(D)); realised = []
    for c, ix in county_idx.items():
        pi = E_i[ix] / E_i[ix].sum()
        v = pi * mult[ix]; v = v / v.sum()
        d[ix] = D.ffs_c.values[ix][0] * pi + S_SHARE * D.mc_c.values[ix][0] * v
        realised.append(v / pi)
    r_ = np.concatenate(realised)
    return d, float(np.std(r_) / np.mean(r_))
field_rows = []
for h_km in (10, 25):
    for sigma in (0.25, 0.5, 1.0):
        rhos, tops, cvs, rhos_ev = [], [], [], []
        for r in range(100):
            dw, cv_ = demand_field(sigma, h_km); cvs.append(cv_)
            A = acc(dw)[idx_S]
            X = np.column_stack([shortfall(A), need_pct])
            r_e = stats.rankdata(-(X @ W_EQ)); r_v = stats.rankdata(-(X @ W_EV))
            rhos.append(stats.spearmanr(r_e, rank["equal"]).statistic); rhos_ev.append(stats.spearmanr(r_v, rank["evidence"]).statistic)
            tops.append(len(set(np.where(r_e <= top10)[0]) & set(np.where(rank["equal"] <= top10)[0])) / top10)
        field_rows.append(dict(field_bandwidth_km=h_km, sigma_log=sigma, realised_cv_share=float(np.mean(cvs)), draws=100, mean_spearman_equal=float(np.mean(rhos)),
                               p5_spearman_equal=float(np.percentile(rhos, 5)), mean_spearman_evidence=float(np.mean(rhos_ev)), top_decile_retention=float(np.mean(tops))))
pd.DataFrame(field_rows).to_csv(TAB / "s06_spatial_field_perturbation.csv", index=False)

# ---- weight-sweep stability at aggregated levels
sw_agg = []
for lv, labs in agg_levels.items():
    if lv == "ZCTA":
        rr = [stats.spearmanr(rank_sw[:, j], rank["equal"]).statistic for j in range(0, NSW, 5)]
    else:
        base = base_agg[lv]
        rr = []
        for j in range(0, NSW, 5):
            ag = agg_rank(comp_sw[:, j], labs)
            rr.append(stats.spearmanr(ag.reindex(base.index).values, base.values).statistic)
    sw_agg.append(dict(level=lv, n_units=int(len(np.unique(labs))), mean_spearman_weight_sweep_vs_equal=float(np.nanmean(rr)), p5=float(np.nanpercentile(rr, 5))))
pd.DataFrame(sw_agg).to_csv(TAB / "s06_weight_sweep_stability_by_unit.csv", index=False)

# ---- random dormancy thinning (status-blind): each provider dormant with prob d
dorm_rows = []
cnt_cols = [f"w_{v}" for v in COMP.values()]
Scount = np.round(pts[cnt_cols].values).astype(int)
for dprob in (0.20, 0.344, 0.50):
    rhos, top_ret = [], []
    for r in range(100):
        St = rng.binomial(Scount, 1 - dprob).astype(float)
        A = acc(base_dw, St)[idx_S]
        X = np.column_stack([shortfall(A), need_pct]) @ W_EQ
        rr = stats.rankdata(-X)
        rhos.append(stats.spearmanr(rr, rank["equal"]).statistic)
        top_ret.append(len(set(np.where(rr <= top10)[0]) & set(np.where(rank["equal"] <= top10)[0])) / top10)
    dorm_rows.append(dict(dormancy_probability=dprob, draws=100, mean_spearman_vs_baseline=float(np.mean(rhos)), p5=float(np.percentile(rhos, 5)), top_decile_retention=float(np.mean(top_ret))))
pd.DataFrame(dorm_rows).to_csv(TAB / "s06_random_dormancy_stability.csv", index=False)

# ---- sensitivity to supply definition (a, b, c, e) with the same baseline demand
def_rows, def_rank = [], {}
for d_ in "abce":
    cols = [f"w_{v.split('__')[0]}__{d_}" for v in COMP.values()]
    A = acc(base_dw, pts[cols].values.astype(float))[idx_S]
    X = np.column_stack([shortfall(A), need_pct]) @ W_EQ
    def_rank[d_] = stats.rankdata(-X)
for d1 in "abce":
    for d2 in "abce":
        if d1 < d2:
            t10a = set(np.where(def_rank[d1] <= top10)[0]); t10b = set(np.where(def_rank[d2] <= top10)[0])
            def_rows.append(dict(def_1=d1, def_2=d2, spearman=float(stats.spearmanr(def_rank[d1], def_rank[d2]).statistic), top_decile_overlap=len(t10a & t10b) / top10))
pd.DataFrame(def_rows).to_csv(TAB / "s06_supply_definition_rank_sensitivity.csv", index=False)

# ---- raw-ratio ranking (the guide's approach) for comparison
raw_rank = stats.rankdata(S["eb_pcp"].values)     # lowest ratio = rank 1
raw_vs = stats.spearmanr(raw_rank, rank["equal"]).statistic
top_raw = set(np.where(raw_rank <= top10)[0]); top_eq = set(np.where(rank["equal"] <= top10)[0])

# ---- final table with tiers
out = pd.DataFrame(index=S.index)
out["county"] = S.county; out["eligibles_2026_09"] = S.elig_primary; out["ruca"] = S.ruca
for j, nme in enumerate(NAMES):
    out[f"shortfall_pct_{nme}"] = X0[:, j]
for nme in schemes:
    out[f"composite_{nme}"] = comp[nme]; out[f"rank_{nme}"] = rank[nme]
out["rank_sweep_median"] = rank_med; out["rank_sweep_p5"] = rank_p5; out["rank_sweep_p95"] = rank_p95
out["top_decile_freq_weight_sweep"] = freq_top_sw
for a in (1000, 100):
    out[f"top_decile_freq_demand_perturb_alpha{a}"] = top_freq_pert[a]
out["top_decile_freq_combined_min"] = np.minimum.reduce([freq_top_sw, top_freq_pert[1000], top_freq_pert[100]])
out["raw_ratio_rank_EB_pcp"] = raw_rank
out["exposure_weighted_rank_equal"] = stats.rankdata(-expo["equal"])
out["exposure_weighted_rank_evidence"] = stats.rankdata(-expo["evidence"])
def tier(f, med):
    if f >= 0.80: return "Tier 1: top decile in >=80% of draws"
    if f >= 0.50: return "Tier 2: top decile in 50-79%"
    if f >= 0.20: return "Tier 3: top decile in 20-49% (possible)"
    return "Not flagged"
out["tier"] = [tier(f, m) for f, m in zip(out.top_decile_freq_combined_min, out.rank_sweep_median)]
out = out.sort_values("rank_sweep_median")
out.reset_index().to_csv(TAB / "s06_gap_ranking_zcta.csv", index=False)
out.reset_index().to_parquet(PROC / "gap_ranking.parquet", index=False)
tiers = out.tier.value_counts()
summ = dict(n=n, top_decile_n=top10, pca_explained_variance=float(pca.explained_variance_ratio_[0]), pca_weights=dict(zip(NAMES, W_PCA.round(3))), evidence_weights=dict(zip(NAMES, W_EV)),
            equal_vs_evidence_spearman=float(stats.spearmanr(rank["equal"], rank["evidence"]).statistic), equal_vs_pca_spearman=float(stats.spearmanr(rank["equal"], rank["pca"]).statistic),
            evidence_vs_pca_spearman=float(stats.spearmanr(rank["evidence"], rank["pca"]).statistic),
            top_decile_overlap_equal_evidence=len(set(np.where(rank["equal"] <= top10)[0]) & set(np.where(rank["evidence"] <= top10)[0])) / top10,
            top_decile_overlap_equal_pca=len(set(np.where(rank["equal"] <= top10)[0]) & set(np.where(rank["pca"] <= top10)[0])) / top10,
            raw_ratio_rank_vs_composite_spearman=float(raw_vs), raw_vs_composite_top_decile_overlap=len(top_raw & top_eq) / top10,
            tier_counts=tiers.to_dict(), sweep_mean_corr_with_equal=float(np.mean(sw_corr)), ranks_with_median_rank_range_gt_50=int(((out.rank_sweep_p95 - out.rank_sweep_p5) > 50).sum()),
            exposure_vs_intensity_spearman=float(stats.spearmanr(out.exposure_weighted_rank_equal, out.rank_equal).statistic),
            baseline_demand="existing FFS + 10% of managed-care members, uniform share within county (IEHP-consistent), Dirichlet perturbation around eligible-proportional shares")
write_json(PROC / "ranking_summary.json", summ)
update_checks("ranking", summ)
pd.set_option("display.width", 220)
print(summ); print(pd.DataFrame(field_rows).round(3).to_string()); print(pert.round(3).T.to_string()); print(pd.DataFrame(sw_agg).round(3)); print(pd.DataFrame(dorm_rows).round(3)); print(pd.DataFrame(def_rows).round(3))
print(out.head(20)[["county", "eligibles_2026_09", "rank_equal", "rank_evidence", "rank_pca", "rank_sweep_median", "rank_sweep_p5", "rank_sweep_p95", "top_decile_freq_weight_sweep", "top_decile_freq_combined_min", "raw_ratio_rank_EB_pcp", "tier"]].round(2).to_string())
