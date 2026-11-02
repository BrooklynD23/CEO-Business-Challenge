"""Step 8: figures (static PNG, light surface). Colours follow the dataviz skill's reference palette: categorical slots in fixed order, one-hue sequential ramp,
text in ink tokens (never series colour), thin marks, recessive grid, direct labels, no dual axes.   [COMPUTED: scripts/analysis/s08_figures.py]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd, geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Patch
from config import *

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
SEQ = LinearSegmentedColormap.from_list("seq", ["#e3eefb", "#9cc3f0", "#2a78d6", "#123f7a"])
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.edgecolor": GRID, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
                     "font.size": 9.5, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left", "legend.frameon": False, "font.family": "DejaVu Sans"})
def save(fig, name):
    fig.savefig(FIG / name, dpi=170, bbox_inches="tight"); plt.close(fig); print("saved", name)

S = pd.read_parquet(PROC / "analysis_sample.parquet").set_index("zcta")
gdf = gpd.read_file(PROC / "zcta_geometry_region.gpkg").set_index("zcta").to_crs(3310)
base = pd.read_parquet(PROC / "base_table.parquet").set_index("zcta")

# ---- F1 primary-care supply by definition (bar) + waterfall
cnt = pd.read_csv(TAB / "s02_supply_counts_by_definition.csv")
wf = pd.read_csv(TAB / "s02_primary_care_waterfall.csv")
fig, ax = plt.subplots(1, 2, figsize=(14, 6.2), gridspec_kw={"width_ratios": [1.2, 1]})
a = ax[0]; w = wf.iloc[1:].copy()
labs = ["(a) candidate\nrows, all\nsources", "drop unknown-\nspecialty\nphysicians", "drop\nProvider_\nSource 3", "drop group\nentities", "dedupe\nNPI-ZIP\n= (b)", "(c) strict", "(d) billable\nat site", "(e) address-\ncap 25"]
vals = w.rows_or_npizip.values
a.bar(range(len(vals)), vals, color=[C1] * len(vals), width=0.62, zorder=3)
for i, v in enumerate(vals): a.text(i, v + 120, f"{v:,.0f}", ha="center", va="bottom", fontsize=8.5, color=INK)
a.set_xticks(range(len(vals))); a.set_xticklabels([l.replace("(a) candidate\nrows, all\nsources","(a) all\ncandidate\nrows").replace("drop unknown-\nspecialty\nphysicians","drop\nunknown\nspecialty") for l in labs], fontsize=7.6); a.set_ylim(0, vals.max() * 1.15)
a.set_title("Primary-care records in the IE extract, step by step\n(physicians with PC specialty + NPs; counts, not people)", fontsize=10.5)
a.set_ylabel("records or unique NPI-ZIP"); a.grid(axis="x", visible=False)
b_ = ax[1]
g = cnt[cnt.group.isin(["pcp", "mh", "specialist_all", "dental (source F)", "clinic_all"])].copy()
lab = {"pcp": "Primary care\n(MD+NP)", "mh": "Mental\nhealth", "specialist_all": "All\nspecialists", "dental (source F)": "Dental\n(F, Oct 2025)", "clinic_all": "Clinics\n(all types)"}
x = np.arange(len(g.group.unique())); width = 0.16
cols = {"a": "#9cc3f0", "b": C1, "c": "#123f7a", "d": C2, "e": "#c98500"}
for k, d_ in enumerate("abcde"):
    vv = [g[(g.group == gg) & (g.definition == d_)].records_or_npizip.iloc[0] for gg in g.group.unique()]
    b_.bar(x + (k - 2) * width, vv, width * 0.92, color=cols[d_], label={"a": "a broad", "b": "b deduped", "c": "c strict", "d": "d billable at site", "e": "e address-capped"}[d_], zorder=3)
b_.set_xticks(x); b_.set_xticklabels([lab[k].replace(" (", "\n(") for k in g.group.unique()], fontsize=7.6); b_.legend(fontsize=8, ncol=2, loc="upper right"); b_.grid(axis="x", visible=False)
b_.set_title("Supply by category and definition (IE counties)", fontsize=10.5); b_.set_ylabel("records or unique NPI-ZIP")
fig.suptitle("Figure 1. How much 'FFS supply' there is depends on the definition (source E, 2026-10-26; F for dental)", x=0.01, y=1.02, ha="left", fontsize=12, fontweight="bold")
save(fig, "f1_supply_definitions.png")

# ---- F2 raw vs catchment scatter
d = S[["eb_pcp", "fca_pcp", "ruca", "elig_primary"]].dropna()
d["raw_pct"] = d.eb_pcp.rank(pct=True); d["fca_pct"] = d.fca_pcp.rank(pct=True)
cls_ = np.where(d.ruca <= 3, "metro (RUCA 1-3)", np.where(d.ruca <= 6, "small town (4-6)", "rural / desert (7-10)"))
fig, ax = plt.subplots(figsize=(6.4, 6.0))
ax.axhspan(0, 0.2, color="#fbe3d8", zorder=0); ax.axvspan(0, 0.2, color="#dbe8f8", zorder=0)
for nm, c in [("metro (RUCA 1-3)", C1), ("small town (4-6)", C4), ("rural / desert (7-10)", C2)]:
    m = cls_ == nm
    ax.scatter(d.raw_pct[m], d.fca_pct[m], s=np.clip(d.elig_primary[m] / 300, 12, 90), color=c, edgecolor=SURF, linewidth=0.8, alpha=0.9, label=f"{nm} (n={m.sum()})", zorder=3)
ax.plot([0, 1], [0, 1], color=MUTED, lw=0.8, ls="--", zorder=2)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xlabel("Raw ratio: FFS primary-care records per 1,000 Medi-Cal eligibles (percentile, EB-shrunk)")
ax.set_ylabel("Catchment (2SFCA, 30 km Gaussian) percentile")
ax.text(0.02, 0.97, "raw says shortage,\ncatchment does not", fontsize=8, color=INK2, va="top"); ax.text(0.5, 0.03, "catchment says shortage, raw does not", fontsize=8, color=INK2)
rho = pd.read_csv(TAB / "s03_raw_vs_catchment_rank_correlation.csv")
r_ = rho[(rho.group == "pcp") & (rho.definition == "b") & (rho.catchment_spec == "g30")].iloc[0]
ax.set_title(f"Figure 2. Raw ratio vs catchment, 130 ZCTAs\nSpearman {r_.spearman:.2f} (95% CI {r_.ci_lo:.2f} to {r_.ci_hi:.2f}); shaded = lowest quintile", fontsize=10.5)
ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3); save(fig, "f2_raw_vs_catchment.png")

# ---- F3 Lorenz
lor = pd.read_pickle(PROC / "lorenz_curves.pkl")
fig, ax = plt.subplots(figsize=(6.2, 5.6))
for (nm, v), c, ls in zip(lor.items(), [C2, "#c98500", C1], ["-", "-", "-"]):
    xs = np.linspace(0, 1, len(v)); ax.plot(xs, v, color=c, lw=1.8, label=nm)
ax.plot([0, 1], [0, 1], color=MUTED, lw=0.8, ls="--")
conc = pd.read_csv(TAB / "s05_supply_concentration_gini.csv")
g_b = conc[(conc.group == "pcp") & (conc.definition == "b")].iloc[0]; g_e = conc[(conc.group == "pcp") & (conc.definition == "e")].iloc[0]; g_el = conc[conc.group.str.startswith("eligibles")].iloc[0]
ax.text(0.02, 0.95, f"PCP records (b): Gini {g_b.gini:.2f}; {int(g_b.zcta_holding_half)} of {int(g_b.n_zcta)} ZCTAs hold half\nAddress-capped (e): Gini {g_e.gini:.2f}; {int(g_e.zcta_holding_half)} ZCTAs hold half\nMedi-Cal eligibles: Gini {g_el.gini:.2f}; {int(g_el.zcta_holding_half)} ZCTAs hold half", fontsize=8.5, va="top", color=INK2)
ax.set_xlabel("cumulative share of ZCTAs (smallest to largest)"); ax.set_ylabel("cumulative share"); ax.legend(loc="center left", bbox_to_anchor=(0.02, 0.55), fontsize=8.5)
ax.set_title("Figure 3. Provider records are far more concentrated\nthan Medi-Cal eligibles (164 IE-assigned ZCTAs)", fontsize=10.5); save(fig, "f3_lorenz.png")

# ---- F4 maps: raw vs catchment
def qmap(ax, series, title, cmap=SEQ, bins=5):
    gg = gdf.loc[gdf.index.intersection(base[base.in_ie_study].index)].copy()
    gg["v"] = series.reindex(gg.index)
    gg.plot(ax=ax, color="#ececE8", edgecolor=SURF, linewidth=0.3)
    h = gg.dropna(subset=["v"]).copy(); h["q"] = pd.qcut(h.v.rank(method="first"), bins, labels=False)
    h.plot(ax=ax, column="q", cmap=cmap, edgecolor=SURF, linewidth=0.3, categorical=False)
    ax.set_axis_off(); ax.set_title(title, fontsize=10)
fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.6))
qmap(ax[0], S.eb_pcp, "Raw: FFS primary-care records per 1,000 Medi-Cal eligibles\n(EB-shrunk; quintiles, darker = more supply)")
qmap(ax[1], S.fca_pcp, "Catchment: 2SFCA accessibility, 30 km Gaussian,\nnearby counties included (quintiles, darker = more access)")
fig.legend(handles=[Patch(color="#e3eefb", label="lowest quintile"), Patch(color="#9cc3f0", label="2nd"), Patch(color="#2a78d6", label="3rd-4th"), Patch(color="#123f7a", label="highest quintile"), Patch(color="#ececE8", label="not ranked (base < 500 eligibles, suppressed, or no polygon)")], loc="lower center", ncol=5, fontsize=8.5, frameon=False)
fig.suptitle("Figure 4. Same supply file, two different pictures (denominator: all Medi-Cal eligibles, 2026-09; straight-line distance proxy)", x=0.01, ha="left", fontsize=12, fontweight="bold")
save(fig, "f4_maps_raw_vs_catchment.png")

# ---- F5 ranking: tiers map + top ranges
rk = pd.read_csv(TAB / "s06_gap_ranking_zcta.csv", dtype={"zcta": str}).set_index("zcta")
tier_col = {"Tier 1: top decile in >=80% of draws": "#a13a12", "Tier 2: top decile in 50-79%": C2, "Tier 3: top decile in 20-49% (possible)": "#f6b79c", "Not flagged": "#e3eefb"}
fig, ax = plt.subplots(1, 2, figsize=(13, 5.8), gridspec_kw={"width_ratios": [1.05, 1]})
gg = gdf.loc[gdf.index.intersection(base[base.in_ie_study].index)].copy(); gg["tier"] = rk.tier.reindex(gg.index)
gg.plot(ax=ax[0], color="#ececE8", edgecolor=SURF, linewidth=0.3)
for t, c in tier_col.items():
    sub = gg[gg.tier == t]
    if len(sub): sub.plot(ax=ax[0], color=c, edgecolor=SURF, linewidth=0.3)
ax[0].set_axis_off(); ax[0].set_title("Tiers: share of 2,000 weight draws x Dirichlet/spatial demand draws\nin which a ZCTA stays in the top decile of general FFS supply shortfall", fontsize=9.5)
ax[0].legend(handles=[Patch(color=c, label=t) for t, c in tier_col.items()] + [Patch(color="#ececE8", label="not ranked")], loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=2, fontsize=7.8, frameon=False)
top = rk.head(20).iloc[::-1]
y = np.arange(len(top))
ax[1].hlines(y, top.rank_sweep_p5, top.rank_sweep_p95, color=C1, lw=2.2, zorder=3)
ax[1].scatter(top.rank_sweep_median, y, color=C1, s=34, zorder=4, edgecolor=SURF)
ax[1].scatter(top.raw_ratio_rank_EB_pcp.clip(upper=60), y, marker="x", color=C2, s=30, zorder=4, label="rank by the guide's raw ratio (lowest = 1)")
ax[1].set_yticks(y); ax[1].set_yticklabels([f"{z}  ({c[:3]})" for z, c in zip(top.index, top.county)], fontsize=8)
ax[1].set_xlabel("rank among 130 ZCTAs (1 = largest shortfall); bar = 5th-95th percentile across weights", labelpad=4); ax[1].set_xlim(0, 62)
ax[1].scatter([], [], color=C1, s=34, label="median rank, weight sweep"); ax[1].legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.45, -0.12), ncol=1)
ax[1].text(61.5, 0, "x at 60 = raw rank 60 or worse", fontsize=7.5, color=INK2, ha="right", va="bottom")
ax[1].set_title("Top 20 ZCTAs: rank ranges, not points", fontsize=10)
fig.suptitle("Figure 5. Preliminary 'general FFS supply shortfall among all Medi-Cal eligibles' ranking (not where movers lose access)", x=0.01, ha="left", fontsize=12, fontweight="bold")
save(fig, "f5_gap_ranking_tiers.png")

# ---- F6 stability
pert = pd.read_csv(TAB / "s06_demand_perturbation_stability.csv"); fld = pd.read_csv(TAB / "s06_spatial_field_perturbation.csv"); dorm = pd.read_csv(TAB / "s06_random_dormancy_stability.csv")
fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.3))
ax[0].plot(pert.realised_cv_of_zcta_transition_share, pert.mean_spearman_vs_baseline_equal_ZCTA, color=C1, marker="o", ms=4.5, lw=1.8, label="ZCTA (n=130)")
ax[0].plot(pert.realised_cv_of_zcta_transition_share, pert["mean_spearman_vs_baseline_equal_4-digit ZIP prefix"], color=C3, marker="o", ms=4.5, lw=1.8, label="4-digit ZIP prefix (39 units)")
ax[0].plot(pert.realised_cv_of_zcta_transition_share, pert["mean_spearman_vs_baseline_equal_ZIP3"], color=C4, marker="o", ms=4.5, lw=1.8, label="ZIP3 (7 units)")
ax[0].set_xlabel("dispersion of ZCTA transition share around uniform\n(coefficient of variation, Dirichlet draws)"); ax[0].set_ylabel("mean Spearman vs baseline ranking"); ax[0].set_ylim(0.85, 1.005)
ax[0].legend(fontsize=8, loc="lower left"); ax[0].set_title("Independent (Dirichlet) unevenness", fontsize=10)
for h_, c in [(10, C1), (25, C2)]:
    f = fld[fld.field_bandwidth_km == h_]
    ax[1].plot(f.realised_cv_share, f.mean_spearman_equal, color=c, marker="o", ms=4.5, lw=1.8, label=f"coherent over ~{h_} km")
ax[1].set_xlabel("dispersion (CV) of the smoothed random field"); ax[1].set_ylim(0.85, 1.005); ax[1].legend(fontsize=8, loc="lower left"); ax[1].set_title("Spatially coherent unevenness (random field)", fontsize=10)
ax[2].plot(range(len(dorm)), dorm.mean_spearman_vs_baseline, color=C1, marker="o", ms=5, lw=1.8, label="mean Spearman vs baseline")
ax[2].plot(range(len(dorm)), dorm.top_decile_retention, color=C2, marker="o", ms=5, lw=1.8, label="share of top decile retained")
ax[2].set_xticks(range(len(dorm))); ax[2].set_xticklabels([f"{int(p*100)}%" for p in dorm.dormancy_probability]); ax[2].set_xlabel("random dormancy probability per provider"); ax[2].set_ylim(0.85, 1.005)
ax[2].set_xlim(-0.3, 2.3); ax[2].legend(fontsize=8, loc="lower left"); ax[2].set_title("Random provider dormancy", fontsize=10)
fig.suptitle("Figure 6. The ranking barely moves under status-blind random perturbation of demand or supply", x=0.01, ha="left", fontsize=12, fontweight="bold")
save(fig, "f6_rank_stability.png")

# ---- F7 extra patients per accepting provider
ep = pd.read_csv(TAB / "s04_extra_patients_per_ffs_provider.csv")
q = ep[(ep.group == "pcp") & (ep.definition.isin(["a", "b", "e"])) & (ep.dormancy.isin([0.0, 0.344]))]
fig, ax = plt.subplots(figsize=(10.5, 5.0))
scen_order = list(SCEN_GUIDE.keys()) + list(SCEN_IEHP.keys())
yy = 0; yt, yl = [], []
for sc in scen_order:
    for d_, dc in [("a", "#9cc3f0"), ("b", C1), ("e", "#c98500")]:
        for dorm_, off, ms in [(0.0, 0.0, "o"), (0.344, 0.0, "D")]:
            r = q[(q.scenario == sc) & (q.definition == d_) & (q.dormancy == dorm_)]
            if r.empty: continue
            r = r.iloc[0]
            ax.hlines(yy + (0.18 if dorm_ else 0), r.extra_per_accepting_provider_lo, r.extra_per_accepting_provider_hi, color=dc, lw=5 if not dorm_ else 2.4, alpha=1.0 if not dorm_ else 0.85, zorder=3)
        yy += 0.62
    yy += 0.5
    yt.append(yy - 0.5 - 0.62 * 3 / 2 - 0.1); yl.append(sc.replace(" (IEHP", "\n(IEHP").replace(" (10%", "\n(10%"))
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=7.8); ax.invert_yaxis(); ax.set_xlabel("extra patients per ACCEPTING primary-care provider, acceptance 65% (left end) to 40% (right end)")
ax.legend(handles=[Patch(color="#9cc3f0", label="a broad (9,778)"), Patch(color=C1, label="b deduped (6,261)"), Patch(color="#c98500", label="e address-capped (3,974)"),
                   plt.Line2D([0], [0], color=INK2, lw=5, label="thick: no dormancy"), plt.Line2D([0], [0], color=INK2, lw=2.4, label="thin: 34% dormant [ESTIMATE, other population]")], fontsize=8, loc="upper center", bbox_to_anchor=(0.45, -0.12), ncol=3)
ax.set_title("Figure 7. Extra patients per accepting primary-care provider (physicians + NPs); IEHP movers only, all-plan movers not included", fontsize=10.5)
ax.grid(axis="y", visible=False); save(fig, "f7_extra_patients_per_provider.png")

# ---- F8 Medicaid_Patients flag
sc = read_json(PROC / "scenario_summary.json"); fl = sc["medicaid_flag"]
fig, ax = plt.subplots(2, 1, figsize=(9.2, 4.6), gridspec_kw={"height_ratios": [1, 1.1]}, sharex=True)
vals = fl["values"]; tot = sum(vals.values()); left = 0
cols_ = {"B": C1, "F": "#9cc3f0", "M": C2, "N": "#a13a12"}
names_ = {"B": "B both", "F": "F FFS only", "M": "M managed care only", "N": "N no new Medicaid"}
for k_ in ["B", "F", "M", "N"]:
    s_ = vals[k_] / tot
    ax[0].barh(0, s_, left=left, color=cols_[k_], height=0.55, edgecolor=SURF, linewidth=2, zorder=3)
    ax[0].text(left + s_ / 2, 0, f"{k_} {s_ * 100:.1f}%" if s_ > 0.06 else f"{k_}\n{s_ * 100:.1f}%", ha="center", va="center", fontsize=8.5, color=INK if k_ == "F" else "white")
    left += s_
ax[0].set_yticks([]); ax[0].grid(False); ax[0].set_title(f"Figure 8. Medicaid_Patients flag: {fl['flagged_rows']:,} of {fl['ie_rows']:,} IE rows ({fl['flagged_share_of_rows']*100:.1f}%), all on billing rows\n(bar = composition of the flagged rows: self-reported 'accepting new Medicaid patients')", fontsize=10)
ax[1].hlines(0.0, 0.40, 0.65, color="#8a8984", lw=9, zorder=2); ax[1].text(0.525, 0.22, "audit range: providers able to offer a new-patient appointment (40-65%)", ha="center", fontsize=8.3, color=INK2)
lo_, hi_ = fl["accept_share_ci95"]; acc_ = fl["share_accept_new_ffs_B_or_F"]
ax[1].hlines(-0.55, lo_, hi_, color=C1, lw=2.2, zorder=3); ax[1].scatter([acc_], [-0.55], color=C1, s=48, zorder=4, edgecolor=SURF)
ax[1].text(acc_, -0.33, f"flagged rows saying B or F: {acc_*100:.1f}% (95% CI {lo_*100:.1f}-{hi_*100:.1f}%)", ha="center", fontsize=8.3, color=INK2)
ax[1].set_ylim(-0.95, 0.6); ax[1].set_yticks([]); ax[1].grid(axis="y", visible=False); ax[1].set_xlim(0, 1)
ax[1].set_xlabel("share (0-1). The two quantities are not the same thing: the flag is self-reported intent on 15% of billing rows; the audit range comes from secret-shopper/survey studies of other states and plans")
ax[1].xaxis.label.set_size(7.6)
save(fig, "f8_medicaid_flag.png")

# ---- F9 forest of key correlation tests
T = pd.read_csv(TAB / "s05_correlation_tests.csv")
keep = ["R1_fca_pcp", "R1_eb_pcp", "R2_fca_pcp", "R2_eb_pcp", "R2_fca_mh", "R3_fca_pcp", "R3_eb_pcp", "R3_fca_mh", "R4_65_pcp", "R4_65_card", "R4_fem_obgyn", "R5_fca_pcp", "R5_eb_pcp",
        "R7_fca_pcp", "R7_fca_mh", "O2_need_pcp", "O2_depr_mh", "O4_novehicle_g30", "O4_novehicle_raw", "O3_fqhc_pcp", "O9_campus_raw"]
lab9 = {"R1_fca_pcp": "enrol. density vs PCP catchment", "R1_eb_pcp": "enrol. density vs raw PCP ratio", "R2_fca_pcp": "poverty vs PCP catchment", "R2_eb_pcp": "poverty vs raw PCP ratio",
        "R2_fca_mh": "poverty vs MH catchment", "R3_fca_pcp": "rurality (RUCA) vs PCP catchment", "R3_eb_pcp": "rurality vs raw PCP ratio", "R3_fca_mh": "rurality vs MH catchment",
        "R4_65_pcp": "share 65+ vs PCP catchment", "R4_65_card": "share 65+ vs cardiology catchment", "R4_fem_obgyn": "women 15-44 vs OB/GYN catchment", "R5_fca_pcp": "limited-English share vs PCP catchment",
        "R5_eb_pcp": "limited-English share vs raw PCP ratio", "R7_fca_pcp": "vulnerability index vs PCP catchment", "R7_fca_mh": "vulnerability index vs MH catchment",
        "O2_need_pcp": "chronic-need index vs PCP catchment", "O2_depr_mh": "depression prevalence vs MH catchment", "O4_novehicle_g30": "no-vehicle HH vs PCP catchment", "O4_novehicle_raw": "no-vehicle HH vs raw PCP ratio",
        "O3_fqhc_pcp": "FQHC site count vs PCP catchment", "O9_campus_raw": "share of PCPs at 100+-NPI addresses vs raw ratio"}
t9 = T.set_index("id").loc[keep].iloc[::-1]
fig, ax = plt.subplots(figsize=(8.8, 7.0)); y = np.arange(len(t9))
sig = t9["significant_adj_0.05"].values
ax.hlines(y, t9.ci_lo, t9.ci_hi, color=np.where(sig, C1, "#b9b8b0"), lw=2, zorder=3)
ax.scatter(t9.estimate, y, color=np.where(sig, C1, "#8a8984"), s=34, zorder=4, edgecolor=SURF)
ax.axvline(0, color=INK2, lw=0.8); ax.set_yticks(y); ax.set_yticklabels([lab9[i] for i in t9.index], fontsize=8.3)
ax.set_xlabel("Spearman rho with 95% bootstrap CI (n about 130); blue = BH-adjusted p < 0.05 across all tests"); ax.set_xlim(-0.9, 0.9)
ax.set_title("Figure 9. Selected correlations (correlation, not cause; ZCTA-level, spatially autocorrelated)", fontsize=10.5); ax.grid(axis="y", visible=False)
save(fig, "f9_correlation_forest.png")

# ---- F10 sanity vs CHCF
sn = pd.read_csv(TAB / "s02_sanity_check_vs_chcf_all_payer.csv")
fig, ax = plt.subplots(figsize=(8.6, 4.6)); x = np.arange(len(sn)); w = 0.36
ax.bar(x - w / 2, sn.E_IE_per_100k, w, color=C1, label="Source E: enrolled FFS physician NPIs", zorder=3)
ax.bar(x + w / 2, sn.CHCF_IE_all_payer_per_100k, w, color=C2, label="CHCF: all-payer physicians (2024)", zorder=3)
for i, r in sn.iterrows(): ax.text(i - w / 2, r.E_IE_per_100k + 3, f"{r.E_IE_per_100k:.0f}", ha="center", fontsize=8.5); ax.text(i + w / 2, r.CHCF_IE_all_payer_per_100k + 3, f"{r.CHCF_IE_all_payer_per_100k:.0f}", ha="center", fontsize=8.5)
ax.set_xticks(x); ax.set_xticklabels([m.replace(" (", "\n(") for m in sn.measure], fontsize=8); ax.set_ylabel("per 100,000 population (IE, 4.77 million)"); ax.legend(fontsize=8.5); ax.grid(axis="x", visible=False)
ax.set_title("Figure 10. 'FFS-enrolled' is nearly the whole physician workforce: E counts match all-payer counts", fontsize=10.5); save(fig, "f10_sanity_check_vs_chcf.png")

# ---- F11 all-plan movers
ap = pd.read_csv(TAB / "s04_all_plan_mover_scenarios.csv")
fig, ax = plt.subplots(figsize=(9.6, 4.8)); names = [k for k in SCEN_GUIDE if k != "Guide mid 1-in-7"] + list(SCEN_IEHP.keys())
for i, nme in enumerate(names):
    r = ap[ap.scenario == nme]
    base_m = r.iloc[0].iucw if False else r.iehp_movers.iloc[0]
    lo = r[r.non_iehp_rate_multiple_of_iehp == 0.5].non_iehp_movers.iloc[0]; mid = r[r.non_iehp_rate_multiple_of_iehp == 1.0].non_iehp_movers.iloc[0]; hi = r[r.non_iehp_rate_multiple_of_iehp == 2.0].non_iehp_movers.iloc[0]
    ax.barh(i, base_m, color=C1, height=0.5, zorder=3, edgecolor=SURF, linewidth=2)
    ax.barh(i, hi, left=base_m, color="#cfe0f6", height=0.5, zorder=2, edgecolor=SURF, linewidth=2)
    ax.barh(i, lo, left=base_m, color=C2, height=0.5, zorder=3, edgecolor=SURF, linewidth=2)
    ax.text(base_m + hi + 3000, i, f"+{lo/1000:.0f}k to +{hi/1000:.0f}k other plans", va="center", fontsize=8.3, color=INK2)
    ax.text(base_m / 2, i, f"{base_m/1000:,.0f}k IEHP", va="center", ha="center", fontsize=8.5, color="white")
ax.set_yticks(range(len(names))); ax.set_yticklabels([n.replace(" (", "\n(") for n in names], fontsize=8); ax.invert_yaxis(); ax.set_xlim(0, 360_000)
ax.set_xlabel("movers (members); orange = non-IEHP plans at 0.5x IEHP's rate, light blue = up to 2.0x"); ax.grid(axis="y", visible=False)
ax.set_title("Figure 11. IEHP-only framing leaves out Kaiser, Molina, SCAN and out-of-county plans (about 374,000 exposed members)", fontsize=10.5)
save(fig, "f11_all_plan_movers.png")
