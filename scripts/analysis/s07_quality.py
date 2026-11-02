"""Step 7: quality checks -> data/quality/checks.json (merged with the sections written by earlier steps) and data/quality/quality_report.md.
[COMPUTED: scripts/analysis/s07_quality.py]"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from config import *

con = duck()
E = RAW / "E_ffs_providers" / "medi-cal-ffs-provider-listing_10_26_26.csv"
chk = read_json(QUAL / "checks.json", {})
q = {}
# ---- filters and dedupe counts vs the data report
r = con.execute(f"""
 with ie as (select * from read_csv('{E}', all_varchar=true, header=true, encoding='latin-1')
             where State='CA' and (County in ('Riverside','San Bernardino') or CountyName in ('Riverside County','San Bernardino County')))
 select count(*) rows_, count(distinct NPI) npi, count(distinct (NPI, upper(trim(Address)), ZIP)) npi_addr_zip,
        count(distinct (NPI, ZIP)) npi_zip from ie""").fetchone()
q["ie_filter"] = dict(rule="State='CA' and (County in (Riverside, San Bernardino) or CountyName in (Riverside County, San Bernardino County))", rows=r[0], unique_npi=r[1], npi_address_zip=r[2], npi_zip=r[3],
                      data_report=dict(rows=36470, unique_npi=30520, npi_address_zip=32529),
                      match=dict(rows=r[0] == 36470, unique_npi=r[1] == 30520, npi_address_zip=r[2] == 32529))
# ---- table keys, joins, label/denominator identities
base = pd.read_parquet(PROC / "base_table.parquet"); acc = pd.read_parquet(PROC / "access_measures.parquet"); cov = pd.read_parquet(PROC / "zcta_covariates.parquet")
rk = pd.read_parquet(PROC / "gap_ranking.parquet"); S = pd.read_parquet(PROC / "analysis_sample.parquet")
q["keys_unique"] = dict(base=bool(base.zcta.is_unique), access=bool(acc.zcta.is_unique), covariates=bool(cov.zcta.is_unique), ranking=bool(rk.zcta.is_unique), sample=bool(S.zcta.is_unique))
q["zip_and_zcta_separate_text_columns"] = bool(base.zip.dropna().str.fullmatch(r"\d{5}").all() and base.zcta.str.fullmatch(r"\d{5}").all())
q["join_coverage_base_169"] = dict(in_A=int(base.in_A.sum()), has_polygon=int(base.has_geometry.sum()), acs_pop=int(cov.pop_acs.gt(0).sum()), acs_poverty=int(cov.poverty_rate.notna().sum()),
                                   acs_income=int(cov.median_hh_income.notna().sum()), places=int(cov.places_diabetes.notna().sum()), ruca=int(cov.ruca.notna().sum()),
                                   catchment_available=int(acc.fca_gvar_pcp__b.notna().sum()), analysis_sample=int(len(S)))
d = acc.set_index("zcta").loc[S.zcta]
ident = (d["n_pcp__b"] / d["elig_2026_09"] * 1000 - d["raw_per1000_pcp__b"]).abs().max()
q["denominator_identity_raw_ratio_max_abs_error"] = float(ident)
q["eligibles_sum_check"] = dict(base_sum_all_touching=float(base.elig_primary.sum()), expected_A_sum=float(chk.get("base_table", {}).get("reconciliation", [{}])[0].get("A_all_ie_touching_zctas_both_counties", np.nan)))
# definition monotonicity: a >= b >= c >= d ; e <= b
sup = pd.read_parquet(PROC / "supply_by_zcta.parquet"); sup.columns = [c[2:] if c.startswith("w_") else c for c in sup.columns]
mono = {}
for g in ["pcp_md", "np", "pcp", "mh", "psychiatrist", "cardiology", "obgyn", "endocrinology", "specialist_all", "clinic_all", "clinic_fqhc"]:
    t = sup.sum()
    mono[g] = bool(t[f"{g}__a"] >= t[f"{g}__b"] >= t[f"{g}__c"] >= t[f"{g}__d"] and t[f"{g}__e"] <= t[f"{g}__b"] + 1e-6)
q["definition_monotonicity"] = mono
# suppression
q["suppression"] = dict(primary_month=PRIMARY_MONTH, suppressed_total_cells_ie_touching=int(base.is_suppressed.sum()), rule="blank+annotation code is 'not shown', never zero; bounds 1-10 stored; suppressed ZCTAs not ranked")
# sensitive-variable guard: no citizenship / nativity / immigration / aid-category columns in any output table or processed parquet
FORBID = re.compile(r"citizen|nativ|foreign|immigra|aid_?categ|uis_|undocument|born", re.I)
bad_cols = []
for f in sorted(TAB.glob("*.csv")):
    cols = pd.read_csv(f, nrows=0).columns
    bad_cols += [f"{f.name}:{c}" for c in cols if FORBID.search(c)]
for f in sorted(PROC.glob("*.parquet")):
    cols = pd.read_parquet(f).columns
    bad_cols += [f"{f.name}:{c}" for c in cols if FORBID.search(c)]
q["sensitive_column_guard"] = dict(forbidden_pattern=FORBID.pattern, offending_columns=bad_cols, passed=len(bad_cols) == 0)
acs_cols = [x for x in pd.read_parquet(PROC / "zcta_covariates.parquet").columns]
q["acs_tables_used"] = ["B01003", "B01001", "B17001", "B19013", "B08201", "C16001 (LEP, access-need only)", "B27001"]
q["no_subcounty_status_estimates"] = "No output allocates, ranks or maps members by immigration status; movers are county-level totals; unevenness tests use status-blind random draws."
# specialty mapping coverage (from s02b)
sd = read_json(PROC / "supply_diagnostics.json", {})
q["specialty_mapping"] = sd.get("specialty_type_coverage", {})
q["definitions"] = {"a": "broad", "b": "deduped NPI-ZIP, individuals, Source 1-2", "c": "strict", "d": "billable at site", "e": "address cap 25"}
# ---- month sensitivity of the denominator (2026-09 primary vs 2026-08 and 2025-09 final)
from scipy import stats
mm = base[base.in_ie_study & base.has_geometry].set_index("zcta")[["elig_2026_09", "elig_2026_08", "elig_2025_09"]].dropna()
mm = mm[mm.elig_2026_09 >= 500]
sup2 = sup.set_index("zcta") if "zcta" in sup.columns else sup
pc = sup2.reindex(mm.index)["pcp__b"].fillna(0)
ms = dict(n=int(len(mm)),
          spearman_eligibles_0908=float(stats.spearmanr(mm.elig_2026_09, mm.elig_2026_08).statistic), spearman_eligibles_0925=float(stats.spearmanr(mm.elig_2026_09, mm.elig_2025_09).statistic),
          median_pct_change_2025_09_to_2026_09=float(100 * (mm.elig_2026_09 / mm.elig_2025_09 - 1).median()), p10_p90_pct_change=[float(x) for x in (100 * (mm.elig_2026_09 / mm.elig_2025_09 - 1)).quantile([.1, .9])],
          total_pct_change_two_counties=float(100 * (mm.elig_2026_09.sum() / mm.elig_2025_09.sum() - 1)),
          spearman_raw_pcp_ratio_0909_vs_0908=float(stats.spearmanr(pc / mm.elig_2026_09, pc / mm.elig_2026_08).statistic),
          spearman_raw_pcp_ratio_0909_vs_2509=float(stats.spearmanr(pc / mm.elig_2026_09, pc / mm.elig_2025_09).statistic))
lo = lambda x: set(x.rank(method="first").nsmallest(int(round(.2 * len(x)))).index)
ms["lowest_quintile_overlap_raw_ratio_vs_2025_09"] = len(lo(pc / mm.elig_2026_09) & lo(pc / mm.elig_2025_09)) / len(lo(pc / mm.elig_2026_09))
q["month_sensitivity"] = ms
chk["quality"] = q
write_json(QUAL / "checks.json", chk)

# ---- human-readable section
b = chk.get("base_table", {}); rc = pd.DataFrame(b.get("reconciliation", []))
lines = ["# Quality checks (Phase 1 analysis)", "", "Generated by `scripts/analysis/s07_quality.py` from `data/quality/checks.json`. Evidence label for everything below: [COMPUTED: scripts/analysis/*.py].", ""]
f = q["ie_filter"]
lines += ["## Filters and dedupe", f"- IE provider filter: {f['rule']}.", f"- Rows {f['rows']:,} (data report 36,470), unique NPI {f['unique_npi']:,} (30,520), NPI-address-ZIP {f['npi_address_zip']:,} (32,529). Matches: {f['match']}.", ""]
lines += ["## Keys and joins", f"- Keys unique: {q['keys_unique']}.", f"- ZIP and ZCTA are separate 5-character text columns: {q['zip_and_zcta_separate_text_columns']}.", f"- Join coverage over the 169 IE-touching ZCTAs: {q['join_coverage_base_169']}.",
          f"- Raw-ratio identity (count / eligibles x 1000) max absolute error {q['denominator_identity_raw_ratio_max_abs_error']:.2e}.", f"- Supply definitions ordered a >= b >= c >= d and e <= b: {q['definition_monotonicity']}.", ""]
if not rc.empty:
    lines += ["## County totals vs source B (all Medi-Cal eligibles)", "```\n" + rc[["month", "county", "B_total", "A_majority_rule", "A_pop_share_alloc", "A_land_share_alloc"]].round(0).to_string(index=False) + "\n```", "",
              f"- The guide's route (sum A over every ZCTA touching the two counties) overshoots B by {b['touching_overshoot']['2026-09']['pct_over']:.2f}% in 2026-09 ({b['touching_overshoot']['2026-09']['A_ie_touching_zctas']:,.0f} vs {b['touching_overshoot']['2026-09']['B_both_counties']:,.0f}); an estimated {b['gap_decomposition_2026_09']['est_members_outside_ie_inside_touching_zctas']:,.0f} members live outside the two counties in split ZCTAs, and population-share allocation closes the gap to within {abs(b['gap_decomposition_2026_09']['residual_B_minus_est_ie_members'])/b['gap_decomposition_2026_09']['B_both_counties']*100:.2f}%.", ""]
lines += ["## Suppression", f"- {q['suppression']}", ""]
lines += ["## Sensitive-variable guard", f"- Offending columns: {q['sensitive_column_guard']['offending_columns']} (passed = {q['sensitive_column_guard']['passed']}).", f"- {q['no_subcounty_status_estimates']}", ""]
sm = q["specialty_mapping"]
lines += ["## Specialty and type mapping (IE extract)", f"- Specialty unknown or N/A: {sm.get('ie_share_spec_unknown_or_NA', np.nan):.1%} of IE rows (statewide {sm.get('statewide_share_spec_unknown_or_NA', np.nan):.1%}; CHCF reported 63.7%).",
          f"- Type unknown or N/A: {sm.get('ie_share_type_unknown_or_NA', np.nan):.1%} of IE rows (statewide {sm.get('statewide_share_type_unknown_or_NA', np.nan):.1%}; CHCF reported 11.1%).",
          f"- Physician rows with no usable specialty after taxonomy/ANC rescue: {sm.get('ie_physician_share_unknown_after_rescue', np.nan):.1%}; {sm.get('ie_physician_rows_rescued_by_taxonomy', 0):,} rows rescued by NUCC taxonomy.", ""]
(QUAL / "quality_report.md").write_text("\n".join(lines))
print(json.dumps(q, indent=1, default=str)[:3500]) if (json := __import__("json")) else None
