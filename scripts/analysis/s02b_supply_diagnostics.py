"""Step 2b: supply diagnostics - definition comparison, address concentration, ORP (Source 3) tests, specialty coverage,
CHCF reconciliation and the all-payer sanity check.   [COMPUTED: scripts/analysis/s02b_supply_diagnostics.py]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from scipy import stats
from config import *

c = pd.read_parquet(PROC / "provider_classified.parquet")
base = pd.read_parquet(PROC / "base_table.parquet")
sup = pd.read_parquet(PROC / "supply_by_zcta.parquet").set_index("zcta")
sup.columns = [x[2:] if x.startswith("w_") else x for x in sup.columns]
ie = c[c.in_ie].copy()
out = {}

# ---------------------------------------------------------------- 1. data-report reproduction + CHCF comparison
out["ie_rows"] = len(ie); out["ie_unique_npi"] = int(ie.npi_key.nunique())
out["ie_unique_npi_addr_zip"] = int(ie[["npi_key", "addr_key", "zip"]].drop_duplicates().shape[0])
by_label = c.groupby("county_label").size()
out["rows_by_County_label"] = {"Riverside": int(by_label.get("Riverside", 0)), "San Bernardino": int(by_label.get("San Bernardino", 0))}
out["rows_by_CountyName_latlon"] = {"Riverside": int((c.county_name == "Riverside County").sum()), "San Bernardino": int((c.county_name == "San Bernardino County").sum())}
out["rows_county_label_NA_total"] = int((c.county_label == "N/A").sum()); out["rows_county_label_UNKNOWN_total"] = int((c.county_label == "UNKNOWN").sum())
out["ie_rows_with_county_label_NA"] = int(((ie.county_label == "N/A")).sum())
chcf = {"Riverside": 13267, "San Bernardino": 14781}
out["chcf_sep25_rows"] = chcf
out["chcf_gap_note"] = ("County-label counts from the 2026-10-26 file are within about 1% of CHCF's 2026-09-25 figures; the 36,470-row IE definition is higher "
                        "because Provider_Source 2/3 rows carry County='N/A' and are only recoverable through CountyName (lat/lon).")

# ---------------------------------------------------------------- 2. Source 3 (ORP) tests
s3 = c[c.source == "3"]; s2 = c[c.source == "2"]; s1 = c[c.source == "1"]
s1_npi = set(s1.npi_key); s3_npi = set(s3.npi_key); s2_npi = set(s2.npi_key)
ie_s3 = ie[ie.source == "3"]
ie_s1_npi = set(ie[ie.source == "1"].npi_key)
orp = dict(
    statewide_rows_source3=int(len(s3)), statewide_npi_source3=int(len(s3_npi)),
    share_source3_rows_non_billing=float((s3.billing == "FFS Non-Billing Provider").mean()),
    share_source3_with_medicaid_flag=float(s3.mcal_flag.notna().mean()),
    share_source3_npi_also_in_source1=float(len(s3_npi & s1_npi) / len(s3_npi)),
    share_source3_npi_also_in_source1_billing=float(len(s3_npi & set(s1[s1.billing == "FFS Billing Provider"].npi_key)) / len(s3_npi)),
    share_source3_type1_individual=float((s3.npi_type == "Type 1").mean()),
    ie_rows_source3=int(len(ie_s3)), ie_source3_npi_not_in_source1_ie=int(len(set(ie_s3.npi_key) - ie_s1_npi)),
    ie_source3_physician_rows=int((ie_s3.ptype == "026").sum()),
    ie_source3_types=ie_s3.ptype.value_counts().head(8).to_dict(),
    statewide_source2_rows=int(len(s2)), share_source2_npi_also_in_source1=float(len(s2_npi & s1_npi) / len(s2_npi)),
    share_source1_rows_billing=float((s1.billing == "FFS Billing Provider").mean()),
    statewide_billing_rows_by_source=c.groupby("source").apply(lambda d: int((d.billing == "FFS Billing Provider").sum())).to_dict(),
    conclusion=("Source 3 rows are all non-billing individuals, none carry the new-patient flag, none carry a taxonomy, and most NPIs appear nowhere in the "
                "billing-capable Main file. That pattern is what ordering/referring/prescribing-only (ORP) records would look like, but the file does not state the "
                "expansion of 'ORP'. They are removed from definitions b-e. UNVERIFIED: the acronym."))
out["orp_source3_test"] = orp

# ---------------------------------------------------------------- 3. specialty/type coverage (CHCF: 63.7% unknown/NA specialty and 11.1% unknown type statewide)
def unk_spec(d): return d.spec.isna()
def unk_type(d): return ~d.has_type
cov = dict(
    statewide_rows=int(len(c)), statewide_share_spec_unknown_or_NA=float(unk_spec(c).mean()), statewide_share_type_unknown_or_NA=float(unk_type(c).mean()),
    ie_rows=int(len(ie)), ie_share_spec_unknown_or_NA=float(unk_spec(ie).mean()), ie_share_type_unknown_or_NA=float(unk_type(ie).mean()),
)
phys = ie[ie.ptype.isin(["026"])]
cov.update(ie_physician_rows=int(len(phys)), ie_physician_share_spec_code_present=float(phys.spec.notna().mean()),
           ie_physician_share_unknown_after_rescue=float((phys.phys_cls == "unknown_specialty").mean()),
           ie_physician_rows_rescued_by_taxonomy=int((phys.class_basis == "taxonomy").sum()), ie_physician_rows_rescued_by_anc=int((phys.class_basis == "anc_type").sum()),
           ie_physician_rows_source3=int((phys.source == "3").sum()))
# primary-care-by-ZIP classifiability: what share of physician+NP rows can be placed in PC vs not-PC vs unknown
pn = ie[ie.ptype.isin(["026", "007"])]
cov["ie_phys_np_rows"] = int(len(pn))
cov["ie_phys_np_rows_primary_care"] = int((pn.g_pcp_md | pn.g_np).sum())
cov["ie_phys_np_rows_specialty_nonPC"] = int((pn.phys_cls.isin(["obgyn", "cardiology", "endocrinology", "other_specialist", "hospital", "psychiatrist"])).sum())
cov["ie_phys_np_rows_unknown_specialty"] = int(pn.g_phys_unknown_spec.sum())
cov["ie_physician_rows_unknown_share_of_candidate_PC_set_a"] = float(ie.g_phys_unknown_spec.sum() / max(1, (ie.g_pcp_md | ie.g_phys_unknown_spec | ie.g_np).sum()))
tcov = (ie.assign(spec_known=ie.spec.notna(), tax_known=ie.tax.notna())
        .groupby(["ptype", "ptype_desc"], dropna=False).agg(rows=("row_id", "size"), npi=("npi_key", "nunique"), spec_known=("spec_known", "sum"),
                                                              classifiable=("classifiable", "sum"), pcp_md=("g_pcp_md", "sum"), unknown_spec_physician=("g_phys_unknown_spec", "sum"))
        .reset_index().sort_values("rows", ascending=False))
tcov.to_csv(TAB / "s02_specialty_type_coverage_ie.csv", index=False)
cov["classifiable_share_all_ie_rows"] = float(ie.classifiable.mean())
cov["unclassifiable_source2_or_3_no_type_rows"] = int((~ie.has_type).sum())
out["specialty_type_coverage"] = cov

# ---------------------------------------------------------------- 4. address concentration
npi_per_addr = ie.groupby("addr_key").npi_key.nunique()
ie["npi_at_addr"] = ie.addr_key.map(npi_per_addr)
def share_at(th, mask=None):
    d = ie if mask is None else ie[mask]
    return float((d.npi_at_addr >= th).mean())
addr = dict(
    ie_unique_addresses=int(len(npi_per_addr)), npi_per_address_median=float(npi_per_addr.median()), npi_per_address_p90=float(npi_per_addr.quantile(.9)),
    npi_per_address_p99=float(npi_per_addr.quantile(.99)), npi_per_address_max=int(npi_per_addr.max()),
    addresses_with_ge50_npi=int((npi_per_addr >= 50).sum()), addresses_with_ge100_npi=int((npi_per_addr >= 100).sum()),
    share_rows_at_addr_ge10=share_at(10), share_rows_at_addr_ge50=share_at(50), share_rows_at_addr_ge100=share_at(100), share_rows_at_addr_ge500=share_at(500),
    share_single_npi_addresses=float((npi_per_addr == 1).mean()),
)
pcb = ie[ie.w_pcp__b > 0]
for th in (10, 25, 50, 100, 500):
    addr[f"pcp_b_share_at_addr_ge{th}"] = float((pcb.npi_at_addr >= th).mean())
addr["pcp_b_total"] = int(len(pcb)); addr["pcp_e_cap25_total"] = float(ie.w_pcp__e.sum())
addr["pcp_cap_reduction_share"] = float(1 - ie.w_pcp__e.sum() / ie.w_pcp__b.sum())
out["address_concentration"] = addr
dist = pd.cut(npi_per_addr, [0, 1, 2, 5, 10, 25, 50, 100, 500, 5000]).value_counts().sort_index()
pd.DataFrame({"npis_at_address_bin": dist.index.astype(str), "n_addresses": dist.values}).to_csv(TAB / "s02_address_npi_distribution.csv", index=False)
# ZCTA-level: share of b-definition PCP at >=100-NPI addresses
pz = pcb.assign(campus=pcb.npi_at_addr >= 100).groupby("zcta").agg(pcp_b=("w_pcp__b", "sum"), pcp_at_campus=("campus", "sum"))
pz["campus_share"] = pz.pcp_at_campus / pz.pcp_b
pz = pz.join(base.set_index("zcta")[["county", "elig_primary"]]).sort_values("pcp_at_campus", ascending=False)
pz.reset_index().to_csv(TAB / "s02_pcp_campus_concentration_by_zcta.csv", index=False)
out["address_concentration"]["n_zcta_with_pcp_b_ge_half_at_100plus_addr"] = int(((pz.campus_share >= 0.5) & (pz.pcp_b >= 10)).sum())

# ---------------------------------------------------------------- 5. definition comparison (counts + ranking)
study = base[base.in_ie_study & (base.elig_primary >= 500) & ~base.is_suppressed & base.has_geometry].set_index("zcta")
GROUPS = ["pcp_md", "np", "pcp", "clinic_all", "mh", "psychiatrist", "cardiology", "obgyn", "endocrinology", "specialist_all", "dental"]
rows, cmp_rows = [], []
for g in GROUPS:
    rate = {}
    for d in "abcde":
        col = f"{g}__{d}"
        if col not in sup.columns: continue
        rate[d] = (sup.loc[study.index, col] / study.elig_primary * 1000)
    R = pd.DataFrame(rate)
    for d1 in R.columns:
        for d2 in R.columns:
            if d1 >= d2: continue
            ok = (R[d1].std() > 0) and (R[d2].std() > 0)
            rho = stats.spearmanr(R[d1], R[d2]).statistic if ok else np.nan
            q1 = set(R[d1].rank(method="first").nsmallest(int(round(.2 * len(R)))).index)
            q2 = set(R[d2].rank(method="first").nsmallest(int(round(.2 * len(R)))).index)
            r1 = R[d1].rank(); r2 = R[d2].rank()
            cmp_rows.append(dict(group=g, def_1=d1, def_2=d2, n_zcta=len(R), spearman=rho, lowest_quintile_overlap=len(q1 & q2) / max(1, len(q1)),
                                 median_abs_rank_change=float((r1 - r2).abs().median()), max_abs_rank_change=float((r1 - r2).abs().max()),
                                 zcta_zero_supply_1=int((R[d1] == 0).sum()), zcta_zero_supply_2=int((R[d2] == 0).sum())))
    for d in R.columns:
        tot = sup.loc[study.index, f"{g}__{d}"].sum()
        rows.append(dict(group=g, definition=d, n_zcta=len(R), supply_total_in_study_zctas=tot, median_per_1000=float(R[d].median()), mean_per_1000=float(R[d].mean()),
                         zcta_with_zero=int((R[d] == 0).sum())))
pd.DataFrame(rows).to_csv(TAB / "s02_supply_definition_summary.csv", index=False)
pd.DataFrame(cmp_rows).to_csv(TAB / "s02_definition_rank_comparison.csv", index=False)

# ---------------------------------------------------------------- 6. all-payer sanity check against CHCF + IEHP network counts
POP_IE = 2_544_916 + 2_224_091       # [VERIFIED: student guide table 1, Census QuickFacts 7/1/2025 est.]
cp = pd.read_csv(RAW / "X_cenpop2020_tract/CenPop2020_Mean_TR06.txt", encoding="utf-8-sig", dtype={"COUNTYFP": str})
POP_CA2020 = int(cp.POPULATION.sum())
def npi_unique(mask, d): return int(d.loc[mask, "npi_key"].nunique())
def physician_metrics(d, label, pop):
    ph = d[d.ptype.eq("026") & d.is_individual]
    s1 = ph[ph.source.isin(["1", "2"])]
    m = dict(scope=label, population=pop,
        physician_npi_all_sources=npi_unique(ph.index == ph.index, ph), physician_npi_source1_2=npi_unique(s1.index == s1.index, s1),
        physician_npi_billing_own=npi_unique(ph.billing.eq("FFS Billing Provider"), ph),
        pc_physician_npi=npi_unique(ph.g_pcp_md, ph), psychiatrist_npi=npi_unique(ph.g_psychiatrist, ph),
        specialist_nonpc_npi=npi_unique(ph.phys_cls.isin(["obgyn", "cardiology", "endocrinology", "other_specialist", "hospital"]), ph),
        unknown_specialty_npi=npi_unique(ph.g_phys_unknown_spec, ph),
        np_npi=npi_unique(d.g_np & d.is_individual, d))
    for k in list(m):
        if k.endswith("_npi") or k.startswith("physician_npi"):
            m[k + "_per_100k"] = m[k] / pop * 1e5
    return m
san = [physician_metrics(ie, "Inland Empire (E, IE extract)", POP_IE)]
cal = c[c.state == "CA"]
san.append(physician_metrics(cal, "California (E, State=CA)", POP_CA2020))
sanity = pd.DataFrame(san)
chcf_rates = {"physicians": (229, 358), "primary_care": (85, 118), "specialty": (115, 176), "psychiatry": (11, 18)}
cmpt = []
ie_m, ca_m = san[0], san[1]
for name, key in [("physicians (all)", "physician_npi_all_sources_per_100k"), ("physicians (Source 1-2 only)", "physician_npi_source1_2_per_100k"),
                  ("primary care physicians", "pc_physician_npi_per_100k"), ("specialists (non-PC, non-psychiatry)", "specialist_nonpc_npi_per_100k"),
                  ("psychiatrists", "psychiatrist_npi_per_100k")]:
    ref = {"physicians (all)": "physicians", "physicians (Source 1-2 only)": "physicians", "primary care physicians": "primary_care",
           "specialists (non-PC, non-psychiatry)": "specialty", "psychiatrists": "psychiatry"}[name]
    cmpt.append(dict(measure=name, E_IE_per_100k=ie_m[key], CHCF_IE_all_payer_per_100k=chcf_rates[ref][0], ratio_E_to_CHCF_IE=ie_m[key] / chcf_rates[ref][0],
                     E_CA_per_100k=ca_m[key], CHCF_CA_per_100k=chcf_rates[ref][1], ratio_E_to_CHCF_CA=ca_m[key] / chcf_rates[ref][1]))
cmpt = pd.DataFrame(cmpt)
cmpt["implied_pc_physicians_chcf_IE"] = 85 / 1e5 * POP_IE
cmpt.to_csv(TAB / "s02_sanity_check_vs_chcf_all_payer.csv", index=False)
sanity.to_csv(TAB / "s02_sanity_inputs_E_physician_counts.csv", index=False)
out["sanity_check_vs_chcf"] = dict(pop_ie=POP_IE, pop_ca_2020_census=POP_CA2020, chcf_pc_implied_ie=85 / 1e5 * POP_IE, rows=cmpt.to_dict("records"),
    ie_E=ie_m, ca_E=ca_m,
    caveats=["CHCF counts active physicians (2024, all payers); E counts enrolled records of any activity level in 2026-10 and cannot see claims.",
             "E physician NPI counted once even if at several addresses; some E physicians practise partly outside the IE.",
             "CHCF 'primary care' definition (specialty grouping) is not given here; E uses FM, IM, pediatrics, GP and geriatrics codes plus taxonomy rescue."])
# IEHP network (fact sheet) vs E definitions
iehp = {"PCP": 1488, "Specialists": 2817, "Behavioral Health": 3453, "Hospitals": 34, "Other": 2570, "Total": 10362}
out["iehp_factsheet_network"] = iehp
out["E_vs_iehp"] = dict(E_pcp_md_b=int(sup["pcp_md__b"].sum()), E_pcp_all_npi=int(ie.loc[ie.g_pcp_md & ie.is_individual, "npi_key"].nunique()),
                        E_specialist_all_b=int(sup["specialist_all__b"].sum()), E_mh_b=int(sup["mh__b"].sum()),
                        note="IEHP counts contracted network practitioners and facilities by their IEHP role (PCP/specialist/behavioral health); E counts FFS-enrolled records by "
                             "type and specialty. Different populations (IEHP network vs FFS enrolment), different units (individual+facility mix vs NPI-ZIP) and different years; ratios are shown only to size the gap.")
# billing structure of PC individuals
pcmask = ie.g_pcp_md & ie.is_individual & ie.source.isin(["1", "2"])
out["pcp_billing_structure"] = dict(n=int(pcmask.sum()), own_npi_billers=float(ie.loc[pcmask, "own_npi_biller"].mean()), billing_row_at_same_address=float(ie.loc[pcmask, "billable_at_site"].mean()))
update_checks("supply_diagnostics", out)
write_json(PROC / "supply_diagnostics.json", out)
print(json.dumps({k: v for k, v in out.items() if k in ("sanity_check_vs_chcf", "address_concentration", "orp_source3_test", "specialty_type_coverage")}, indent=1, default=str)[:6000]) if (json := __import__("json")) else None
print(cmpt.round(2).to_string())
