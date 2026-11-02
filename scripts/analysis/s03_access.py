"""Step 3: the core ratio (FFS providers per 1,000 Medi-Cal eligibles) and why it misleads - two-step floating catchment area.

DENOMINATOR for every ratio here: all Medi-Cal certified eligibles (managed care + FFS + other plans) in the ZCTA, source A, 2026-09 (preliminary).
It is NOT movers, NOT IEHP members and NOT existing FFS members.  Numerators: FFS-enrolled provider records/NPI-ZIP counts by definition a-e (s02).
Distances are straight-line (planar, EPSG:3310) between ZCTA population-weighted points and provider coordinates - a PROXY, not travel time.
Catchment demand and supply include every CA ZCTA / provider inside 150 km of an IE ZCTA (LA, Orange, San Diego, Imperial, Kern, Inyo, Ventura, ...) and
border providers in NV/AZ (they have no Medi-Cal demand because demand is California residents only).
[COMPUTED: scripts/analysis/s03_access.py]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd, geopandas as gpd
from scipy import stats, sparse, optimize, special
from scipy.spatial import cKDTree
from config import *

base = pd.read_parquet(PROC / "base_table.parquet")
dem = pd.read_parquet(PROC / "zcta_demand_region.parquet")
pts = pd.read_parquet(PROC / "supply_points_region.parquet")
sup = pd.read_parquet(PROC / "supply_by_zcta.parquet").set_index("zcta")
sup.columns = [x[2:] if x.startswith("w_") else x for x in sup.columns]
cls = pd.read_parquet(PROC / "provider_classified.parquet")

GROUPS = ["pcp_md", "np", "pcp", "clinic_all", "mh", "psychiatrist", "cardiology", "obgyn", "endocrinology", "specialist_all", "dental"]
DEFS = list("abcde")

# --------------------------------------------------------------------------- RUCA class of each region ZCTA (via same-digit ZIP)
ruca = pd.read_csv(RAW / "X_usda_ruca_zip/2020-rural-urban-commuting-area-codes-zip-codes.csv", dtype=str)
ruca = ruca.rename(columns={"ZIPCode": "zcta", "PrimaryRUCA": "ruca"})
ruca["ruca"] = pd.to_numeric(ruca.ruca, errors="coerce")
dem = dem.merge(ruca[["zcta", "ruca"]].drop_duplicates("zcta"), on="zcta", how="left")
dem["ruca_filled"] = dem.ruca.fillna(4)
dem["radius_var_km"] = np.where(dem.ruca_filled <= 3, 15.0, np.where(dem.ruca_filled <= 6, 30.0, 60.0))
dem["d0_var"] = dem.radius_var_km * 1000.0

# --------------------------------------------------------------------------- denominators and county multipliers for the scenario-demand variant
con = duck()
B2 = RAW / "B_delivery_plan/t2_eligibility_by_delivery_system_plan_201001_oct2026.csv"
b = con.execute(f"""select County as county, "Health Delivery System" as sys, {num('"Total Eligibles"')} as n from read_csv('{B2}', all_varchar=true, header=true)
                    where "Month of Eligibility"='2026-09' and County<>'STATEWIDE'""").df()
b["n"] = b.n.astype("float64")
bc = b.groupby(["county", "sys"]).n.sum().unstack().fillna(0.0)
bc["ffs_share"] = bc["Fee-for-Service"] / (bc["Fee-for-Service"] + bc["Managed Care"])
cty = gpd.read_file(f"zip://{RAW / 'X_tiger_county_2020' / 'cb_2020_us_county_500k.zip'}")
fips2name = cty[cty.STATEFP == "06"].set_index("GEOID").NAME.to_dict()
dem["county_name2"] = dem.county_fips.map(fips2name)
S_MOVE = 1 / 7                            # guide's middle scenario, applied to managed-care members, uniformly within county
bc["scen_mult"] = (bc["Fee-for-Service"] + S_MOVE * bc["Managed Care"]) / (bc["Fee-for-Service"] + bc["Managed Care"])
dem["scen_mult"] = dem.county_name2.map(bc.scen_mult).fillna(bc.scen_mult.median())

# --------------------------------------------------------------------------- core ratio by ZCTA (IE-touching) + minimum base + empirical Bayes
study = base.set_index("zcta")
core = pd.DataFrame(index=study.index)
core["county"] = study.county; core["in_ie_study"] = study.in_ie_study; core["is_split_zcta"] = study.is_split_zcta
core["elig_2026_09"] = study.elig_primary; core["is_suppressed"] = study.is_suppressed
core["elig_2026_08"] = study.elig_2026_08; core["elig_2025_09"] = study.elig_2025_09
core["has_geometry"] = study.has_geometry
core["min_base_ok"] = (study.elig_primary >= 500) & study.has_geometry
MIN_BASE = 500

def eb_fit(y, e):
    """Poisson-gamma empirical Bayes: y_i ~ Poisson(lambda_i e_i), lambda ~ Gamma(shape a, rate b). Returns a, b, posterior means."""
    y = np.asarray(y, float); e = np.asarray(e, float)
    def nll(p):
        a, bb = np.exp(p)
        ll = special.gammaln(y + a) - special.gammaln(a) - special.gammaln(y + 1) + a * np.log(bb / (bb + e)) + y * np.log(e / (bb + e))
        return -ll.sum()
    m = y.sum() / e.sum()
    best = None
    for a0 in (0.5, 1.0, 3.0, 10.0):
        r = optimize.minimize(nll, np.log([a0, a0 / max(m, 1e-6)]), method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-9, "maxiter": 4000})
        if best is None or r.fun < best.fun: best = r
    a, bb = np.exp(best.x)
    return a, bb, (y + a) / (e + bb)

eb_params = {}
ok = study.in_ie_study & study.has_geometry & study.elig_primary.notna() & (study.elig_primary > 0)
for g in GROUPS:
    for d in DEFS:
        col = f"{g}__{d}"
        if col not in sup.columns: continue
        y = sup.reindex(study.index)[col].fillna(0.0)
        core[f"n_{col}"] = y
        core[f"raw_per1000_{col}"] = np.where(study.elig_primary > 0, y / study.elig_primary * 1000, np.nan)
        e = study.loc[ok, "elig_primary"].values / 1000.0
        a, bb, post = eb_fit(np.round(y[ok].values), e)
        core.loc[ok, f"eb_per1000_{col}"] = post
        eb_params[col] = dict(shape=float(a), rate=float(bb), prior_mean_per1000=float(a / bb), prior_cv=float(1 / np.sqrt(a)))

# --------------------------------------------------------------------------- 2SFCA machinery
D = dem[dem.is_ca_demand & (dem.elig_2026_09_imputed > 0)].reset_index(drop=True)      # demand locations
dx = D[["x", "y"]].values
sx = pts[["lx", "ly"]].values
RMAX = 60_000.0
td, ts = cKDTree(dx), cKDTree(sx)
rec = td.sparse_distance_matrix(ts, RMAX, output_type="ndarray")
I, J, dist = rec["i"].astype(np.int64), rec["j"].astype(np.int64), rec["v"].astype(float)
print("pairs within", RMAX / 1000, "km:", len(I), "| demand points", len(D), "| supply locations", len(pts))

def kernel(dist, d0, kind):
    inside = dist <= d0
    if kind == "step":
        w = inside.astype(float)
    else:
        w = (np.exp(-0.5 * (dist / d0) ** 2) - np.exp(-0.5)) / (1 - np.exp(-0.5))
        w = np.where(inside, w, 0.0)
    return w

def fca(dem_weight, supply_matrix, d0_per_pair, kind, I=I, J=J, dist=dist, n_d=len(D), n_s=len(pts)):
    """Two-step floating catchment. dem_weight: (n_d,), supply_matrix: (n_s, k). d0_per_pair per pair. Returns (n_d,k) accessibility per demand unit."""
    w = kernel(dist, d0_per_pair, kind)
    keep = w > 0
    Wm = sparse.csr_matrix((w[keep], (I[keep], J[keep])), shape=(n_d, n_s))
    denom = Wm.T @ dem_weight                               # n_s : weighted demand competing for each provider location
    R = np.divide(supply_matrix, denom[:, None], out=np.zeros_like(supply_matrix), where=denom[:, None] > 0)
    return Wm @ R

# columns of supply to evaluate
def sup_cols(groups, defs):
    cols = []
    for g in groups:
        for d in defs:
            c = f"w_{g}__{d}"
            if c in pts.columns: cols.append(c)
    return cols

all_cols = sup_cols(GROUPS, DEFS)
S_all = pts[all_cols].values.astype(float)
dw = D.elig_2026_09_imputed.values.astype(float)
SPECS = {"gvar": ("gauss", None), "g15": ("gauss", 15e3), "g30": ("gauss", 30e3), "g50": ("gauss", 50e3),
         "step10": ("step", 10e3), "step20": ("step", 20e3), "step30": ("step", 30e3), "step50": ("step", 50e3)}
catch = {}
for name, (kind, rad) in SPECS.items():
    d0pp = D.d0_var.values[I] if rad is None else np.full(len(I), rad)
    A = fca(dw, S_all, d0pp, kind)
    catch[name] = pd.DataFrame(A * 1000.0, index=D.zcta, columns=[c[2:] for c in all_cols])
# scenario demand variant (existing FFS + 1/7 of managed care, uniform within county) with the primary spec
dw_s = dw * D.scen_mult.values
Ascen = fca(dw_s, S_all, D.d0_var.values[I], "gauss")
catch["gvar_scenario"] = pd.DataFrame(Ascen * 1000.0, index=D.zcta, columns=[c[2:] for c in all_cols])
# sensitivity: add NV/AZ/OR border providers (no competing demand is available for them -> upper-bound-like)
ptsB = pd.read_parquet(PROC / "supply_points_region_with_border_states.parquet")
tsB = cKDTree(ptsB[["lx", "ly"]].values)
recB = td.sparse_distance_matrix(tsB, RMAX, output_type="ndarray")
IB, JB, dB = recB["i"].astype(np.int64), recB["j"].astype(np.int64), recB["v"].astype(float)
AB = fca(dw, ptsB[all_cols].values.astype(float), D.d0_var.values[IB], "gauss", I=IB, J=JB, dist=dB, n_d=len(D), n_s=len(ptsB))
catch["gvar_with_border_states"] = pd.DataFrame(AB * 1000.0, index=D.zcta, columns=[c[2:] for c in all_cols])
# IE-only truncation (what a county-filtered analysis would do): demand only ZCTAs assigned to IE; supply only providers in IE ZCTAs
ie_zcta = set(base[base.in_ie_study].zcta)
cl = cls[cls.loc_x.notna() & cls.zcta.isin(ie_zcta)].copy()
cl["lx"] = cl.loc_x.round(0); cl["ly"] = cl.loc_y.round(0)
wcols = [c for c in cls.columns if c.startswith("w_") and not c.startswith("w_dental")]
ptsIE = cl.groupby(["lx", "ly"])[wcols].sum().reset_index()
dentalIE = pd.read_parquet(PROC / "dental_classified.parquet")
dentalIE = dentalIE[dentalIE.zcta.isin(ie_zcta) & dentalIE.loc_x.notna()].copy()
dentalIE["lx"] = dentalIE.loc_x.round(0); dentalIE["ly"] = dentalIE.loc_y.round(0)
dpts = dentalIE.groupby(["lx", "ly"])[[c for c in dentalIE.columns if c.startswith("w_")]].sum().reset_index()
ptsIE = ptsIE.merge(dpts, on=["lx", "ly"], how="outer").fillna(0.0)
DIE = D[D.zcta.isin(ie_zcta)].reset_index(drop=True)
tdI, tsI = cKDTree(DIE[["x", "y"]].values), cKDTree(ptsIE[["lx", "ly"]].values)
recI = tdI.sparse_distance_matrix(tsI, RMAX, output_type="ndarray")
II, JJ, dd = recI["i"].astype(np.int64), recI["j"].astype(np.int64), recI["v"].astype(float)
colsI = [c for c in all_cols if c in ptsIE.columns]
AI = fca(DIE.elig_2026_09_imputed.values.astype(float), ptsIE[colsI].values.astype(float), DIE.d0_var.values[II], "gauss", I=II, J=JJ, dist=dd, n_d=len(DIE), n_s=len(ptsIE))
catch["gvar_ie_only"] = pd.DataFrame(AI * 1000.0, index=DIE.zcta, columns=[c[2:] for c in colsI])

# --------------------------------------------------------------------------- assemble wide table for IE-touching ZCTAs
out = core.copy()
_new = {}
KEEP_SPEC_FULL = ["gvar", "gvar_scenario", "gvar_ie_only", "gvar_with_border_states"]
KEEP_SPEC_GROUPS = list(GROUPS)
for name, tab in catch.items():
    t = tab.reindex(out.index)
    for col in t.columns:
        g_, d_ = col.split("__")
        if name in KEEP_SPEC_FULL or (g_ in KEEP_SPEC_GROUPS and d_ in ("b", "c")):
            _new[f"fca_{name}_{col}"] = t[col]
out = pd.concat([out, pd.DataFrame(_new)], axis=1)
# whole-region catchment table (all demand ZCTAs: IE and neighbours) for the IE-vs-neighbours comparison
reg_out = []
for name in ("gvar", "g30"):
    t = catch[name].copy(); t.columns = [f"{name}__{c}" for c in t.columns]; reg_out.append(t)
reg_fca = pd.concat(reg_out, axis=1)
reg_fca = reg_fca.join(D.set_index("zcta")[["county_name2", "county_fips", "elig_2026_09_imputed", "ruca", "pw_lat", "pw_lon"]])
reg_fca.reset_index().to_parquet(PROC / "region_fca.parquet", index=False)
# context for interpretation
ctx = dem.set_index("zcta")[["ruca", "radius_var_km", "dist_to_ie_km", "county_fips"]]
out = out.join(ctx.rename(columns={"county_fips": "county_fips_major"}))
out.reset_index().to_parquet(PROC / "access_measures.parquet", index=False)
out.reset_index().to_csv(TAB / "s03_access_measures_by_zcta.csv", index=False)
write_json(PROC / "eb_params.json", eb_params)

# --------------------------------------------------------------------------- raw vs catchment: correlations, flips, border, radii
st = out[out.in_ie_study & out.min_base_ok & ~out.is_suppressed].copy()
rows = []
for g in GROUPS:
    for d in ("a", "b", "c"):
        raw = f"raw_per1000_{g}__{d}"
        if raw not in st.columns: continue
        for spec in ["gvar", "g15", "g30", "g50", "step10", "step20", "step30", "step50", "gvar_scenario", "gvar_ie_only", "gvar_with_border_states"]:
            f = f"fca_{spec}_{g}__{d}"
            if f not in st.columns: continue
            sub = st[[raw, f]].dropna()
            if len(sub) < 20 or sub[raw].std() == 0 or sub[f].std() == 0: continue
            rho, p = stats.spearmanr(sub[raw], sub[f])
            rng = np.random.default_rng(SEED)
            bs = [stats.spearmanr(*sub.sample(len(sub), replace=True, random_state=int(rng.integers(1e9))).T.values).statistic for _ in range(400)]
            q = int(round(0.2 * len(sub)))
            lo_raw = set(sub[raw].rank(method="first").nsmallest(q).index); lo_f = set(sub[f].rank(method="first").nsmallest(q).index)
            rows.append(dict(group=g, definition=d, catchment_spec=spec, n=len(sub), spearman=rho, ci_lo=np.nanpercentile(bs, 2.5), ci_hi=np.nanpercentile(bs, 97.5),
                             lowest_quintile_overlap=len(lo_raw & lo_f) / max(1, q), median_abs_rank_change=float((sub[raw].rank() - sub[f].rank()).abs().median())))
rc = pd.DataFrame(rows)
rc.to_csv(TAB / "s03_raw_vs_catchment_rank_correlation.csv", index=False)

# flips for primary care physicians + NPs, definition b, primary catchment spec
g, d = "pcp", "b"
raw, f = f"raw_per1000_{g}__{d}", f"fca_gvar_{g}__{d}"
sub = st[[raw, f, "county", "ruca", "radius_var_km", "elig_2026_09", f"n_{g}__{d}", "dist_to_ie_km"]].dropna(subset=[raw, f]).copy()
sub["raw_rank_pct"] = sub[raw].rank(pct=True); sub["fca_rank_pct"] = sub[f].rank(pct=True)
sub["flip_class"] = np.select([(sub.raw_rank_pct <= .2) & (sub.fca_rank_pct > .4), (sub.raw_rank_pct > .4) & (sub.fca_rank_pct <= .2),
                               (sub.raw_rank_pct <= .2) & (sub.fca_rank_pct <= .2)],
                              ["raw says shortage, catchment does not (false alarm)", "catchment says shortage, raw does not (hidden)", "both low"], "other")
sub = sub.sort_values("raw_rank_pct")
sub.reset_index().to_csv(TAB / "s03_rank_flips_primary_care.csv", index=False)
flip_counts = sub.flip_class.value_counts().to_dict()

# border effect: catchment with neighbours vs IE-only truncation
bf = st[[f"fca_gvar_pcp__b", f"fca_gvar_ie_only_pcp__b", "dist_to_ie_km", "county", "ruca"]].dropna()
bf["pct_change"] = 100 * (bf["fca_gvar_ie_only_pcp__b"] / bf["fca_gvar_pcp__b"] - 1)
bf.reset_index().to_csv(TAB / "s03_border_effect_primary_care.csv", index=False)
# border = ZCTA within 15 km (planar) of a non-IE-assigned ZCTA point (neighbour county or outside CA)
nonie = dem[~dem.zcta.isin(ie_zcta) & dem.is_ca_demand]
tn = cKDTree(nonie[["x", "y"]].values)
dd_nb = tn.query(dem.set_index("zcta").loc[bf.index, ["x", "y"]].values)[0] / 1000
bf["km_to_nearest_non_ie_zcta_point"] = dd_nb
bf["border"] = bf.km_to_nearest_non_ie_zcta_point <= 12
border_summary = bf.groupby("border")["pct_change"].describe()
border_summary.to_csv(TAB / "s03_border_effect_summary.csv")

# urban vs desert contrast
def ruca_class(r): return "metro (RUCA 1-3)" if r <= 3 else ("small town (4-6)" if r <= 6 else "rural/desert (7-10)")
st["ruca_class"] = st.ruca.fillna(4).map(ruca_class)
ud = st.groupby(["county", "ruca_class"]).agg(n_zcta=("elig_2026_09", "size"), eligibles=("elig_2026_09", "sum"),
        raw_pcp_b_per1000_median=("raw_per1000_pcp__b", "median"), fca_gvar_pcp_b_median=("fca_gvar_pcp__b", "median"),
        fca_g15_pcp_b_median=("fca_g15_pcp__b", "median"), fca_g30_pcp_b_median=("fca_g30_pcp__b", "median"), fca_g50_pcp_b_median=("fca_g50_pcp__b", "median")).reset_index()
ud.to_csv(TAB / "s03_urban_desert_contrast.csv", index=False)

# radius sensitivity: rank correlation among catchment specs (pcp b)
sp_cols = [f"fca_{s}_pcp__b" for s in ["gvar", "g15", "g30", "g50", "step10", "step20", "step30", "step50"] if f"fca_{s}_pcp__b" in st.columns]
rho_mat = st[sp_cols].corr(method="spearman")
rho_mat.to_csv(TAB / "s03_radius_spec_spearman_pcp_b.csv")

# example ZCTAs (area-level, no provider detail): Chino-area vs desert
ex = ["91710", "91761", "92277", "92242", "92363", "92252", "92225", "92354", "92505"]
exd = out.reindex([z for z in ex if z in out.index])[["county", "elig_2026_09", "ruca", "n_pcp__b", "raw_per1000_pcp__b", "fca_g15_pcp__b", "fca_g30_pcp__b", "fca_g50_pcp__b", "fca_gvar_pcp__b"]]
exd.reset_index().to_csv(TAB / "s03_example_zcta_radius_sensitivity.csv", index=False)

update_checks("access", dict(
    min_base=MIN_BASE, n_study_zcta_ie=int(out.in_ie_study.sum()), n_ranked_zcta=int(len(st)), n_below_min_base=int((~out.min_base_ok & out.in_ie_study).sum()),
    demand_points=int(len(D)), supply_locations=int(len(pts)), pairs_within_60km=int(len(I)), kernel="Gaussian E2SFCA (Dai 2010) with RUCA-variable catchment 15/30/60 km (primary)",
    flip_counts_pcp_b=flip_counts, eb_prior_example={k: eb_params[k] for k in ["pcp__b", "mh__b", "specialist_all__b"] if k in eb_params},
    rank_correlation_pcp_b_gvar=float(rc[(rc.group == "pcp") & (rc.definition == "b") & (rc.catchment_spec == "gvar")].spearman.iloc[0]),
))
pd.set_option("display.width", 220)
print(rc[(rc.definition == "b") & rc.catchment_spec.isin(["gvar", "g30", "gvar_ie_only"])].round(3).to_string())
print(flip_counts); print(border_summary.round(1)); print(ud.round(2).to_string()); print(exd.round(2).to_string()); print(rho_mat.round(2))
