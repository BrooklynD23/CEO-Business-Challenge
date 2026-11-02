"""Step 4: scenarios - movers, FFS growth, all-plan demand, extra patients per FFS provider, required acceptance, Medicaid_Patients flag.

Sensitive-population rule: scenario movers are county/regional totals applied uniformly; nothing here allocates movers below county level.
Primary scenario set (policy_verification.md section 2): IEHP Governing Board 2026-08-10: Low 100,000, Mid 132,000, High 155,000.
Comparison set: the guide's illustrative 10% / 14% / 1-in-7 / 18% of 1,321,983 (exceeds IEHP's own statement).
[COMPUTED: scripts/analysis/s04_scenarios.py]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from scipy import stats
from config import *

con = duck()
B2 = RAW / "B_delivery_plan/t2_eligibility_by_delivery_system_plan_201001_oct2026.csv"
b = con.execute(f"""select "Month of Eligibility" as month, County as county, "Health Delivery System" as sys, "Health Plan" as plan,
                    {num('"Total Eligibles"')} as n, "Annotation Code" as ann, Status as status
                    from read_csv('{B2}', all_varchar=true, header=true)""").df()
b["n"] = b.n.astype("float64")
cls = pd.read_parquet(PROC / "provider_classified.parquet")
ie = cls[cls.in_ie]
chk = {}

# ------------------------------------------------------------------ scenario movers
BASE = IEHP_MEDICAL_FACTSHEET
iehp_b = b[(b.month == "2026-09") & b.county.isin(["Riverside", "San Bernardino"]) & b.plan.str.startswith("Inland Empire Health Plan", na=False)]
IEHP_B = float(iehp_b.n.sum())
prim = [(k, v, v / BASE, v / IEHP_B, v / IEHP_ALL_PROGRAMS) for k, v in SCEN_PRIMARY.items()]
guide = [(k, round(BASE * s), s, round(BASE * s) / IEHP_B, round(BASE * s) / IEHP_ALL_PROGRAMS) for k, s in SCEN_GUIDE.items()]
sc = pd.DataFrame([("primary (IEHP board 2026-08-10)", *r) for r in prim] + [("guide illustrative (exceeds IEHP statement)", *r) for r in guide],
                  columns=["set", "scenario", "movers", "share_of_1321983_factsheet_medical", "share_of_B_iehp_members_2026_09", "share_of_all_programs_1394246"])
guide_check = dict(
    guide_text="about 190,000 at about 14% (1 in 7)", at_14_0_pct=round(BASE * 0.14), at_1_in_7=round(BASE / 7), guide_190k_implies_share=190_000 / BASE,
    diff_190k_vs_14pct=190_000 - round(BASE * 0.14), diff_190k_vs_1_in_7=190_000 - round(BASE / 7),
    rounding_note="190,000 implies 14.37%; 14.0% gives 185,078 (about 185,000); exactly 1/7 gives 188,855 (about 189,000). The guide overstates its own 'about 14%' row by 1,100-5,000 members.")
# county split of IEHP members (uniform-share assumption, county level only)
iehp_cty = iehp_b.groupby("county").n.sum()
sc["riverside_if_split_by_iehp_members"] = sc.movers * iehp_cty["Riverside"] / IEHP_B
sc["san_bernardino_if_split_by_iehp_members"] = sc.movers * iehp_cty["San Bernardino"] / IEHP_B
sc.to_csv(TAB / "s04_scenarios_movers.csv", index=False)

# ------------------------------------------------------------------ existing FFS members and revision/lag
ffs = b[(b.sys == "Fee-for-Service") & b.county.isin(["Riverside", "San Bernardino"])].pivot_table(index="month", columns="county", values="n", aggfunc="sum")
ffs["total"] = ffs.sum(axis=1)
ffs_status = b[(b.sys == "Fee-for-Service") & (b.county == "Riverside")].groupby("month").status.first()
ffs["status"] = ffs_status
ffs.to_csv(TAB / "s04_existing_ffs_series_two_counties.csv")
ffs_sep = float(ffs.loc["2026-09", "total"]); ffs_aug = float(ffs.loc["2026-08", "total"]); ffs_oct = float(ffs.loc["2026-10", "total"])
mature = float(ffs.loc[["2026-06", "2026-07", "2026-08"], "total"].mean())
st = b[(b.county == "STATEWIDE") | (b.county != "STATEWIDE")]
allc = b[b.county != "STATEWIDE"]
state_ffs = allc[allc.sys == "Fee-for-Service"].groupby("month").n.sum()
state_mc = allc[allc.sys == "Managed Care"].groupby("month").n.sum()
dhcs_apr = dict(ffs=702_547, mc=13_207_633)       # [VERIFIED: S01 per research/policy_verification.md, DHCS figures for April 2026; vintage date not stated]
vint = dict(
    ffs_two_counties_2026_09_as_published=ffs_sep, ffs_two_counties_2026_08=ffs_aug, ffs_two_counties_2026_10=ffs_oct,
    mature_proxy_mean_2026_06_to_08=mature, sep_vs_mature_shortfall_pct=100 * (1 - ffs_sep / mature), oct_vs_mature_shortfall_pct=100 * (1 - ffs_oct / mature),
    statewide_ffs_2026_04_in_oct7_snapshot=float(state_ffs["2026-04"]), statewide_mc_2026_04_in_oct7_snapshot=float(state_mc["2026-04"]),
    dhcs_quoted_2026_04=dhcs_apr, ffs_revision_pct_between_dhcs_quote_and_oct7_snapshot=100 * (float(state_ffs["2026-04"]) / dhcs_apr["ffs"] - 1),
    mc_revision_pct=100 * (float(state_mc["2026-04"]) / dhcs_apr["mc"] - 1),
    older_vintages_available="No. Only the 2026-10-07 snapshot of A/B was downloaded; the Internet Archive was offline (HTTP 'Temporarily Offline') on 2026-11-02, so no older B vintage could be fetched. "
                             "Evidence of upward revision comes from (i) the within-snapshot recency profile and (ii) DHCS's own April-2026 figure (vintage date not stated) vs the same month in this snapshot.",
)
chk["vintage"] = vint
# the within-snapshot lag profile, statewide (months with F status are matured)
prof = pd.DataFrame({"statewide_ffs": state_ffs, "statewide_mc": state_mc}).loc["2025-06":]
prof["ffs_over_trailing_3mo_mean_prior"] = prof.statewide_ffs / prof.statewide_ffs.shift(1).rolling(3).mean()
prof.to_csv(TAB / "s04_statewide_ffs_recency_profile.csv")

# FFS growth in each scenario (two counties). FFS base 1: as published; base 2: lag-adjusted estimate.
rows = []
for name, M in list(SCEN_PRIMARY.items()) + [(k, round(BASE * s)) for k, s in SCEN_GUIDE.items()]:
    for lab, base_ffs in [("as published 2026-09 (prelim.)", ffs_sep), ("lag-adjusted (mean 2026-06..08) [ESTIMATE]", mature)]:
        rows.append(dict(scenario=name, movers=M, existing_ffs_base=lab, existing_ffs=base_ffs, movers_per_existing_ffs=M / base_ffs, ffs_population_multiple=(base_ffs + M) / base_ffs,
                         set="primary" if name in SCEN_PRIMARY else "guide"))
growth = pd.DataFrame(rows)
growth.to_csv(TAB / "s04_ffs_growth_iehp_only.csv", index=False)

# ------------------------------------------------------------------ all-plan demand
mc = b[(b.month == "2026-09") & (b.sys == "Managed Care") & b.county.isin(["Riverside", "San Bernardino"])].copy()
def plan_group(p):
    if not isinstance(p, str): return "other"
    if p.startswith("Inland Empire Health Plan"): return "IEHP"
    if p.startswith("Molina"): return "Molina"
    if p.startswith("Kaiser"): return "Kaiser"
    if "PACE" in p or p.startswith("WelbeHealth") or p.startswith("InnovAge"): return "PACE (stays in PACE)"
    if p.startswith("SCAN"): return "SCAN (Medi-Medi dual plan)"
    if p.startswith("Out of County"): return "Out-of-county plan"
    return "other"
mc["pg"] = mc.plan.map(plan_group)
plan_tab = mc.pivot_table(index="pg", columns="county", values="n", aggfunc="sum")
plan_tab["total"] = plan_tab.sum(axis=1)
plan_tab["suppressed_cells"] = mc[mc.n.isna()].groupby("pg").size().reindex(plan_tab.index).fillna(0)
plan_tab["share_of_managed_care"] = plan_tab.total / plan_tab.total.sum()
plan_tab.to_csv(TAB / "s04_managed_care_by_plan_two_counties_2026_09.csv")
MC_TOTAL = float(plan_tab.total.sum())
non_iehp_exposed = float(plan_tab.loc[["Molina", "Kaiser", "SCAN (Medi-Medi dual plan)", "Out-of-county plan"], "total"].sum())
iehp_members_B = float(plan_tab.loc["IEHP", "total"])
# statewide cross-check: IEHP 5-7% of 2M movers with 10.0% of enrollment (policy_verification.md sec 2)
impl = {}
for sh in (0.05, 0.07):
    impl[f"iehp_mover_share_{int(sh*100)}pct"] = (1 - sh) / 0.90 / (sh / 0.10)     # non-IEHP rate / IEHP rate, per member, statewide
mults = [0.5, 1.0, 1.5, 2.0]
rows = []
for name, M in list(SCEN_PRIMARY.items()) + [(k, round(BASE * s)) for k, s in SCEN_GUIDE.items()]:
    r = M / BASE
    for m in mults:
        non = non_iehp_exposed * r * m
        tot = M + non
        rows.append(dict(set="primary" if name in SCEN_PRIMARY else "guide", scenario=name, iehp_movers=M, iehp_rate=r, non_iehp_rate_multiple_of_iehp=m,
                         non_iehp_movers=non, all_plan_movers=tot, understatement_pct_of_all_plan=100 * non / tot, all_plan_over_iehp_only_pct=100 * non / M,
                         ffs_multiple_all_plan_published_base=(ffs_sep + tot) / ffs_sep, ffs_multiple_all_plan_lag_adj_base=(mature + tot) / mature))
allplan = pd.DataFrame(rows)
allplan.to_csv(TAB / "s04_all_plan_mover_scenarios.csv", index=False)
chk["all_plan"] = dict(managed_care_total_B_2026_09=MC_TOTAL, iehp_members_B=iehp_members_B, iehp_share_of_mc=iehp_members_B / MC_TOTAL,
                       non_iehp_exposed_members=non_iehp_exposed, statewide_implied_rate_multiples=impl,
                       note="Kaiser, Molina, SCAN and out-of-county plan members counted as exposed; PACE excluded (stays in PACE). Multiples 0.5-2.0 are a range, not an estimate. "
                            "Statewide pattern (IEHP 10.0% of enrolment, 5-7% of movers) implies non-IEHP plans' per-member rate 1.5x-2.1x IEHP's [ESTIMATE: arithmetic on S35/S32].")

# ------------------------------------------------------------------ extra patients per FFS provider
GROUPS = {"pcp_md": "primary care physicians", "pcp": "primary care physicians + NPs", "np": "nurse practitioners", "clinic_fqhc": "FQHC/RHC sites (035)", "clinic_all": "clinic sites (all clinic types)"}
DEFN = {"a": "broad", "b": "deduped", "c": "strict", "d": "billable at site", "e": "address-capped"}
N = {(g, d): float(ie[f"w_{g}__{d}"].sum()) for g in GROUPS for d in DEFN}
DORM = [0.0, 0.20, 0.344, 0.45]     # 0.344 = 45,000 / (45,000+86,000) statewide plan-serving enrolled providers [ESTIMATE: S35 arithmetic; different population]
rows = []
scen_all = list(SCEN_PRIMARY.items()) + [(k, round(BASE * s)) for k, s in SCEN_GUIDE.items()]
for (g, d), n in N.items():
    for name, M in scen_all:
        for dorm in DORM:
            lo = M / (n * (1 - dorm) * ACCEPT_HI)
            hi = M / (n * (1 - dorm) * ACCEPT_LO)
            mid = M / (n * (1 - dorm) * 0.525)
            rows.append(dict(group=g, group_label=GROUPS[g], definition=d, definition_label=DEFN[d], providers=n, dormancy=dorm, scenario=name, movers=M,
                             set="primary" if name in SCEN_PRIMARY else "guide", extra_per_provider_all_accept=M / n, extra_per_accepting_provider_lo=lo, extra_per_accepting_provider_mid=mid,
                             extra_per_accepting_provider_hi=hi,
                             extra_per_provider_if_quarter_carry=M / (n * (1 - dorm) * 0.25)))
epp = pd.DataFrame(rows)
epp.to_csv(TAB / "s04_extra_patients_per_ffs_provider.csv", index=False)
# existing load per provider (FFS members / provider record)
existing_load = pd.DataFrame([dict(group=g, definition=d, providers=n, existing_ffs_per_provider_published=ffs_sep / n, existing_ffs_per_provider_lag_adj=mature / n) for (g, d), n in N.items()])
existing_load.to_csv(TAB / "s04_existing_ffs_members_per_provider.csv", index=False)

# the other way round: acceptance rate needed so that extra patients per accepting provider <= h, and h as a share of a panel benchmark
PANELS = {"Altschuler team-based low 1,387": 1387, "Altschuler team-based high 1,947": 1947, "US average panel ~2,300 (UNVERIFIED)": 2300}
H = [25, 50, 100, 200]
rows = []
for (g, d), n in N.items():
    if g not in ("pcp_md", "pcp"): continue
    for name, M in scen_all:
        for h in H:
            need = M / (n * h)
            rows.append(dict(group=g, definition=d, scenario=name, set="primary" if name in SCEN_PRIMARY else "guide", movers=M, providers=n, added_panel_per_accepting_provider=h,
                             required_acceptance_rate=need, feasible_at_65pct=bool(need <= ACCEPT_HI), feasible_at_100pct=bool(need <= 1.0),
                             h_as_pct_of_panel_1387=100 * h / 1387, h_as_pct_of_panel_1947=100 * h / 1947, h_as_pct_of_panel_2300=100 * h / 2300))
req = pd.DataFrame(rows)
req.to_csv(TAB / "s04_required_acceptance_or_added_panel.csv", index=False)
# required added panel at the audit-range acceptance rates, vs benchmark
rows = []
for (g, d), n in N.items():
    if g not in ("pcp_md", "pcp"): continue
    for name, M in scen_all:
        for a in (0.40, 0.525, 0.65, 1.0):
            h = M / (n * a)
            rows.append(dict(group=g, definition=d, scenario=name, set="primary" if name in SCEN_PRIMARY else "guide", acceptance=a, added_panel_needed=h,
                             pct_of_panel_1387=100 * h / 1387, pct_of_panel_1947=100 * h / 1947, pct_of_panel_2300=100 * h / 2300))
pd.DataFrame(rows).to_csv(TAB / "s04_added_panel_vs_benchmark.csv", index=False)

# ------------------------------------------------------------------ Medicaid_Patients flag
fl = ie[ie.mcal_flag.notna()]
fvc = fl.mcal_flag.value_counts()
share_accept = float((fvc.get("B", 0) + fvc.get("F", 0)) / len(fl))
share_ffs_only_or_both = share_accept
share_mc_only = float(fvc.get("M", 0) / len(fl)); share_n = float(fvc.get("N", 0) / len(fl))
fl_stat = dict(ie_rows=int(len(ie)), flagged_rows=int(len(fl)), flagged_share_of_rows=float(len(fl) / len(ie)), values=fvc.to_dict(),
               share_accept_new_ffs_B_or_F=share_accept, share_managed_care_only_M=share_mc_only, share_no_new_medicaid_N=share_n,
               share_declining_new_ffs_M_or_N=share_mc_only + share_n,
               audit_range=[ACCEPT_LO, ACCEPT_HI], gap_above_audit_top_pp=100 * (share_accept - ACCEPT_HI), gap_above_audit_bottom_pp=100 * (share_accept - ACCEPT_LO))
# binomial CI for the accept share
from scipy.stats import beta
k, n_ = int(fvc.get("B", 0) + fvc.get("F", 0)), len(fl)
fl_stat["accept_share_ci95"] = [float(beta.ppf(.025, k, n_ - k + 1)), float(beta.ppf(.975, k + 1, n_ - k))]
bill = ie[ie.billing == "FFS Billing Provider"]
fl_stat["billing_rows"] = int(len(bill)); fl_stat["flag_coverage_of_billing_rows"] = float(bill.mcal_flag.notna().mean())
fl_stat["nonbilling_flagged_rows"] = int(ie[ie.billing != "FFS Billing Provider"].mcal_flag.notna().sum())
# selection: who carries the flag (type mix) vs billing rows without it
tm = bill.assign(flagged=bill.mcal_flag.notna()).groupby(["ptype", "ptype_desc"], dropna=False).agg(rows=("row_id", "size"), flagged=("flagged", "sum")).reset_index()
tm["flagged_share"] = tm.flagged / tm.rows
tm = tm.sort_values("rows", ascending=False)
tm.to_csv(TAB / "s04_medicaid_flag_coverage_by_type.csv", index=False)
by_val_type = fl.groupby(["ptype", "mcal_flag"]).size().unstack(fill_value=0)
by_val_type["n"] = by_val_type.sum(axis=1)
by_val_type["accept_ffs_share"] = (by_val_type.get("B", 0) + by_val_type.get("F", 0)) / by_val_type.n
by_val_type.sort_values("n", ascending=False).head(15).to_csv(TAB / "s04_medicaid_flag_values_by_type.csv")
# PC-specific
pcfl = ie[(ie.w_pcp__b > 0) | ((ie.g_pcp_md | ie.g_np) & ie.mcal_flag.notna())]
fl_stat["pcp_rows_b"] = int((ie.w_pcp__b > 0).sum()); fl_stat["pcp_b_rows_with_flag"] = int(((ie.w_pcp__b > 0) & ie.mcal_flag.notna()).sum())
pcp_any = ie[(ie.g_pcp_md | ie.g_np | ie.ptype.isin(["022", "010"]) & (ie.g_pcp_md | ie.g_np)) & ie.mcal_flag.notna()]
fl_stat["pcp_any_flagged_rows"] = int(len(pcp_any)); fl_stat["pcp_any_flag_values"] = pcp_any.mcal_flag.value_counts().to_dict()
fl_stat["pcp_any_accept_share"] = float(pcp_any.mcal_flag.isin(["B", "F"]).mean()) if len(pcp_any) else None
# county and address-size selection among billing rows
bill = bill.assign(flagged=bill.mcal_flag.notna())
addr_n = ie.groupby("addr_key").npi_key.nunique()
bill["npi_at_addr"] = bill.addr_key.map(addr_n)
sel = bill.groupby("flagged").agg(rows=("row_id", "size"), share_type2_org=("npi_type", lambda s: float((s == "Type 2").mean())),
                                 share_riverside=("ie_county", lambda s: float((s == "Riverside").mean())), median_npi_at_addr=("npi_at_addr", "median"),
                                 share_telehealth_Y=("telehealth", lambda s: float((s == "Y").mean())))
sel.to_csv(TAB / "s04_medicaid_flag_selection_billing_rows.csv")
# logistic regression: flagged ~ type group + county + org + log address size  (billing rows)
import statsmodels.api as sm
Xd = pd.DataFrame({"flagged": bill.flagged.astype(int).values, "org": (bill.npi_type == "Type 2").astype(int).values,
                   "sb": (bill.ie_county == "San Bernardino").astype(int).values, "log_addr_npi": np.log1p(bill.npi_at_addr.values),
                   "phys": bill.ptype.eq("026").astype(int).values, "mh": bill.ptype.isin(["077", "070", "031", "103"]).astype(int).values,
                   "clinic": bill.ptype.isin(["035", "041", "045", "048", "096", "075"]).astype(int).values}, index=bill.index)
Xm = sm.add_constant(Xd.drop(columns="flagged"))
lg = sm.Logit(Xd.flagged, Xm).fit(disp=0, cov_type="HC1")
lgt = pd.DataFrame({"coef": lg.params, "or": np.exp(lg.params), "ci_lo": np.exp(lg.conf_int()[0]), "ci_hi": np.exp(lg.conf_int()[1]), "p": lg.pvalues})
lgt.to_csv(TAB / "s04_medicaid_flag_selection_logit.csv")
fl_stat["selection_logit_n"] = int(len(Xd)); fl_stat["selection_logit"] = lgt.round(4).to_dict("index")
# acceptance among flagged by county
fl_stat["accept_share_by_county"] = fl.groupby("ie_county").mcal_flag.apply(lambda s: float(s.isin(["B", "F"]).mean())).to_dict()
# FFS-accepting flagged count as upper bound of "known accepting" supply
fl_stat["known_accepting_new_ffs_rows"] = int(fvc.get("B", 0) + fvc.get("F", 0))
fl_stat["interpretation_M"] = ("M = accepts new managed-care Medicaid patients only. These records are FFS-enrolled (they are in E) but declare no new FFS patients: "
                               "a partial view of providers on the guide's Group A list who would not take moving members. N = no new Medicaid at all. "
                               "Because the flag is self-reported, present on 15% of billing rows and on no non-billing IE row, M+N is a floor on declining providers, not a rate.")
chk["medicaid_flag"] = fl_stat

# ------------------------------------------------------------------ age-structure ranges (statewide shares only; policy S31)
age = dict(under21_share=251_000 / 1_900_000, age50plus_share_of_expansion=0.288)
ar = []
for name, M in scen_all:
    ar.append(dict(scenario=name, movers=M, under21_est=M * age["under21_share"], age50plus_est=M * age["age50plus_share_of_expansion"]))
pd.DataFrame(ar).to_csv(TAB / "s04_age_share_ranges_statewide_shares.csv", index=False)
chk["age_shares_note"] = "Statewide shares (251,000 of 1.9 million under 21; 28.8% age 50+ of the expansion group) applied to IEHP scenarios; ESTIMATE, not an IE count; no age restriction on demand."

write_json(PROC / "scenario_summary.json", dict(guide_check=guide_check, **chk))
update_checks("scenarios", dict(guide_check=guide_check, iehp_B_members=IEHP_B, **chk))
pd.set_option("display.width", 230); pd.set_option("display.max_columns", 30)
print(sc.round(3).to_string()); print(guide_check); print(vint); print(growth[growth.existing_ffs_base.str.startswith("as")].round(2).to_string())
print(plan_tab.round(0).to_string()); print(allplan[(allplan.non_iehp_rate_multiple_of_iehp.isin([0.5, 1, 2])) & (allplan.set == "primary")].round(2).to_string())
print(epp[(epp.group == "pcp") & (epp.definition.isin(["a", "b", "c"])) & (epp.dormancy == 0) & (epp.set == "primary")].round(1).to_string())
print(fl_stat)
print(lgt.round(3))
