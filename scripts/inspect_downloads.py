#!/usr/bin/env python
"""Profile the raw downloads (read-only) and write data/catalog/inspection_summary.txt.

Run:  $HOME/.venvs/iehp-access/bin/python -I scripts/inspect_downloads.py

Reads files under data/raw/ with DuckDB. Never modifies them. All counts quoted in
research/data_acquisition_report.md come from this script's output.
Only counting and schema checks are done here; no correlation analysis, no sub-county
estimate of immigration status (contract rule 2).
"""
from __future__ import annotations

import warnings
from pathlib import Path

import duckdb

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "catalog" / "inspection_summary.txt"
IE = "('06065','06071')"

con = duckdb.connect()
lines: list[str] = []


def p(s: str = "") -> None:
    lines.append(s)


def q(title: str, sql: str, n: int = 60) -> None:
    p(f"-- {title}")
    try:
        df = con.execute(sql).fetchdf()
        p(df.to_string(index=False) if len(df) <= n else df.head(n).to_string(index=False) + f"\n... ({len(df)} rows)")
    except Exception as e:  # noqa: BLE001
        p(f"ERROR: {e}")
    p()


def first(pattern: str) -> str:
    hits = sorted(RAW.glob(pattern))
    return str(hits[0]) if hits else ""


# ------------------------------------------------------------------ views
fA = first("A_zip_eligibles_2020_recent/*.csv")
fE = first("E_ffs_providers/medi-cal-ffs-provider-listing*.csv")
fF = first("F_dental_ffs_providers/ffsproviderprofile*.csv")
fH = first("H_census_zcta_county/*.txt")
fD = first("D_managed_care_enrollment/*.csv")
num = 'try_cast(replace(trim("Total Eligibles"),\',\',\'\') as bigint)'

con.execute(f"create view a as select \"Month of Eligibility\" m, trim(\"Zip Code\") zip, Sex, {num} n, "
            f"\"Annotation Code\" ac, Status, \"Date of Data\" dod from read_csv('{fA}', all_varchar=true)")
con.execute(f"create view rel as select * from read_csv('{fH}', delim='|', all_varchar=true)")
con.execute("create view ie_z as select GEOID_ZCTA5_20 z, GEOID_COUNTY_20 cty, try_cast(AREALAND_PART as double) a "
            f"from rel where coalesce(GEOID_ZCTA5_20,'')<>'' and GEOID_COUNTY_20 in {IE}")
con.execute("create view allz as select GEOID_ZCTA5_20 z, GEOID_COUNTY_20 cty, try_cast(AREALAND_PART as double) a "
            "from rel where coalesce(GEOID_ZCTA5_20,'')<>''")
con.execute(f"create view e0 as select *, substr(trim(ZIP),1,5) zip5 from read_csv('{fE}', all_varchar=true, encoding='latin-1')")
con.execute("create view e_ie as select * from e0 where State='CA' and (County in ('Riverside','San Bernardino') "
            "or CountyName in ('Riverside County','San Bernardino County'))")
con.execute(f"create view f as select * from read_csv('{fF}', all_varchar=true)")
con.execute(f"create view d as select \"Enrollment Month\" m, \"Plan Type\" pt, County, \"Plan Name\" plan, "
            "try_cast(replace(trim(\"Count of Enrollees\"),',','') as bigint) n, \"Count of Enrollees Annotation Code\" ac "
            f"from read_csv('{fD}', header=true, all_varchar=true)")

# ------------------------------------------------------------------ A
p("=== SOURCE A: Medi-Cal certified eligibles by ZIP (2020-recent)")
q("rows, n_months, range", "select count(*) rows, count(distinct m) n_months, min(m) first_m, max(m) last_m from a")
q("status by month range", "select Status, min(m) mn, max(m) mx, count(distinct m) n_months, min(dod) dod_min, max(dod) dod_max from a group by 1")
q("months present around 2025-10 gap", "select distinct m from a where m between '2025-08' and '2025-12' order by 1")
q("rows per recent month", "select m, count(*) rows, count(distinct zip) zips, max(dod) data_date from a where m>='2026-06' group by 1 order by 1")
q("annotations", "select ac, count(*) from a group by 1")
q("non-numeric zip values", "select zip, count(*) from a where not regexp_matches(zip,'^[0-9]{5}$') group by 1")
q("statewide total by month (zip='STATEWIDE', Total)", "select m, n from a where zip='STATEWIDE' and sex='Total' and m>='2026-01' order by 1")
q("IE-touching ZCTAs (Census 2020 rel file) count", "select count(distinct z) zctas_touching_ie from ie_z")
q("ZCTA county split", """with t as (select z, sum(a) tot, sum(case when cty in ('06065','06071') then a else 0 end) ie, count(distinct cty) nc
 from allz where z in (select z from ie_z) group by z)
 select count(*) zctas, sum(case when nc>1 then 1 else 0 end) multi_county, sum(case when ie/tot>=0.5 then 1 else 0 end) ie_area_majority from t""")
q("IE-touching ZCTA presence in A and suppression", """select m, count(*) zips, sum(case when n is null then 1 else 0 end) suppressed_total_cells, sum(n) total
 from a where sex='Total' and zip in (select z from ie_z) and m in ('2026-08','2026-09','2026-10') group by 1 order by 1""")
q("IE ZCTAs absent from A in 2026-09", "select z from (select distinct z from ie_z) where z not in (select zip from a where m='2026-09')")
q("Total = Female+Male check (2026-09, IE ZCTAs)", """select count(*) mismatches from (select zip, max(case when sex='Total' then n end) t,
 sum(case when sex in ('Female','Male') then n end) fm from a where zip in (select z from ie_z) and m='2026-09' group by zip)
 where t is not null and fm is not null and t<>fm""")
q("suppressed cells by sex/code (2026-09 IE ZCTAs)", "select sex, ac, count(*) n from a where zip in (select z from ie_z) and m='2026-09' and n is null group by all")

# ------------------------------------------------------------------ B / D
def bview(name: str, key: str) -> None:
    f = first(f"{key}/*.csv")
    con.execute(f"create view {name} as select *, {num} n from read_csv('{f}', all_varchar=true, header=true)")


p("=== SOURCE B (age/sex, language, delivery system+plan, race/ethnicity)")
bview("b_age", "B_age_sex"); bview("b_lang", "B_language"); bview("b_plan", "B_delivery_plan"); bview("b_race", "B_race_ethnicity")
for nm in ("b_age", "b_lang", "b_plan", "b_race"):
    q(f"{nm} rows/range/status", f"select count(*) rows, min(\"Month of Eligibility\") mn, max(\"Month of Eligibility\") mx, count(distinct County) counties, "
      f"sum(case when n is null and \"Annotation Code\" is not null then 1 else 0 end) suppressed_cells from {nm}")
q("B plan: IE delivery system by month", """select "Month of Eligibility" m, County, "Health Delivery System" sys, sum(n) total, sum(case when n is null then 1 else 0 end) suppressed
 from b_plan where County in ('Riverside','San Bernardino') and "Month of Eligibility" in ('2026-08','2026-09','2026-10') group by all order by 2,1,3""")
q("B plan: IEHP rows (2026-09)", """select County, "Health Plan", "Total Eligibles" from b_plan where "Month of Eligibility"='2026-09' and "Health Plan" like 'Inland Empire%' order by 1""")
q("B age/sex IE 2026-09", """select County, "Age Group", Gender, "Total Eligibles" from b_age where County in ('Riverside','San Bernardino') and "Month of Eligibility"='2026-09' order by 1,2,3""")
q("B language distinct values", "select distinct Language from b_lang order by 1", 60)
q("B race distinct values", "select distinct Ethnicity from b_race order by 1")

p("=== SOURCE D: managed care enrollment (header=true needed; BOM + trailing comma)")
q("D range", "select min(m) mn, max(m) mx, count(*) rows, count(distinct m) n_months from d")
q("D IE by county, plan type (2026-09, non-dental)", """select County, pt, plan, n, ac from d where m='2026-09' and County in ('Riverside','San Bernardino') order by 1,2,3""")
q("D IE managed-care total 2026-09", "select County, sum(n) total from d where m='2026-09' and County in ('Riverside','San Bernardino') and pt<>'Dental' group by 1")

# ------------------------------------------------------------------ E
p("=== SOURCE E: Medi-Cal FFS providers (as of 2026-10-26)")
q("overall", "select count(*) rows, count(distinct NPI) npi, count(distinct Provider_Number) provider_numbers, count(distinct Provider_Number||'|'||Service_Location_Number) pn_loc from e0")
q("county column coverage", "select County, count(*) n from e0 where County in ('Riverside','San Bernardino','N/A','UNKNOWN') group by 1 order by 2 desc")
q("IE rows by County/CountyName (State=CA)", "select County, CountyName, count(*) n from e_ie group by all order by 3 desc")
q("County='N/A' IE rows by Provider_Source", "select Provider_Source, count(*) n from e_ie where County='N/A' group by 1")
q("IE rows vs unique NPIs", "select count(*) rows, count(distinct NPI) npi, count(distinct Provider_Number) pn, count(distinct NPI||'|'||Address||'|'||zip5) npi_address from e_ie")
q("IE rows excluding Provider_Source 3 (ORP)", "select count(*) rows, count(distinct NPI) npi from e_ie where Provider_Source<>'3'")
q("IE NPI repeat distribution", "select rows_per_npi, count(*) npis from (select NPI, count(*) rows_per_npi from e_ie group by 1) group by 1 order by 1 limit 10")
q("Provider_Source x Billing_Provider x Medicaid_Patients populated (statewide)", """select Provider_Source, Billing_Provider, (Medicaid_Patients is not null) mcp_populated, count(*) from e0 group by all order by 1,2,3""")
q("IE Medicaid_Patients (accepting new patients flag) values", "select Medicaid_Patients, count(*) n from e_ie group by 1 order by 2 desc")
q("IE provider types", "select FI_Provider_Type_CD cd, FI_Provider_Type type, count(*) rows, count(distinct NPI) npi from e_ie group by all order by 3 desc", 40)
q("IE physician specialties", """select FI_Provider_Specialty_CD cd, FI_Provider_Specialty sp, count(*) rows, count(distinct NPI) npi from e_ie
 where FI_Provider_Type_CD='026' group by all order by 3 desc""", 25)
q("Clinic/FQHC provider types statewide (CA)", """select FI_Provider_Type_CD cd, FI_Provider_Type, count(*) rows from e0 where State='CA'
 and FI_Provider_Type_CD in ('035','040','041','045','048','075','096') group by all order by 1""")
q("IE clinic types", """select FI_Provider_Type_CD cd, FI_Provider_Type, count(*) rows, count(distinct NPI) npi from e_ie
 where FI_Provider_Type_CD in ('035','040','041','045','048','075','096') group by all order by 1""")
q("IE rows whose ZIP is inside an IE-touching ZCTA", "select count(*) rows, sum(case when zip5 in (select z from ie_z) then 1 else 0 end) in_ie_zcta from e_ie")
q("Latest enrollment effective date", "select max(strptime(split_part(Enroll_Status_Eff_DT,' ',1),'%m/%d/%Y')) latest_eff, min(strptime(split_part(Enroll_Status_Eff_DT,' ',1),'%m/%d/%Y')) earliest from e0")
q("E county mismatch: County vs CountyName (both IE but differ)", """select count(*) from e0 where State='CA' and ((County='Riverside' and CountyName='San Bernardino County') or (County='San Bernardino' and CountyName='Riverside County'))""")

# ------------------------------------------------------------------ F
p("=== SOURCE F: dental FFS providers and safety net clinics (as of 2025-10)")
q("overall", "select count(*) rows, count(distinct \"Provider NPI\") npi from f")
q("types", "select \"Provider Type Code\" cd, \"Provider Type Code Desc\" d, count(*) rows, count(distinct \"Provider NPI\") npi from f group by all order by 3 desc")
q("IE", "select \"Provider County Desc\" county, count(*) rows, count(distinct \"Provider NPI\") npi from f where \"Provider County Desc\" in ('Riverside','San Bernardino') group by 1")
q("blank county rows", "select count(*) from f where \"Provider County Desc\" is null or trim(\"Provider County Desc\")=''")

# ------------------------------------------------------------------ G
p("=== SOURCE G: HRSA HPSA (header has trailing comma -> null_padding)")
for tag, rel_f in (("PC", "G_hpsa_primary_care/*.csv"), ("MH", "G_hpsa_mental_health/*.csv"), ("DH", "G_hpsa_dental/*.csv")):
    f = first(rel_f)
    con.execute(f"""create or replace view g as select * from read_csv('{f}', all_varchar=true, header=true, delim=',', quote='"', escape='"', null_padding=true)""")
    q(f"{tag} rows and IE designations by status", """select "HPSA Status" status, count(*) component_rows, count(distinct "HPSA ID") hpsa_ids, max("Data Warehouse Record Create Date Text") dw_date
 from g where "Common State Abbreviation"='CA' and regexp_matches("Common County Name",'Riverside|San Bernardino') group by 1""")
    q(f"{tag} IE Designated: ZIP blank share", """select count(*) rows, sum(case when "HPSA Postal Code" is null or trim("HPSA Postal Code")='' then 1 else 0 end) blank_zip,
 min(try_cast("HPSA Score" as int)) min_score, max(try_cast("HPSA Score" as int)) max_score from g where "HPSA Status"='Designated' and "Common State Abbreviation"='CA'
 and regexp_matches("Common County Name",'Riverside|San Bernardino')""")

# ------------------------------------------------------------------ others
p("=== OTHER")
h = first("X_hrsa_health_center_sites/*.csv")
con.execute(f"create view hc as select * from read_csv('{h}', all_varchar=true, header=true, null_padding=true)")
q("HRSA health center sites in IE", """select "Complete County Name" county, "Health Center Type Description" t, "Health Center Service Delivery Site Location Setting Description" s, count(*) n from hc
 where "Site State Abbreviation"='CA' and regexp_matches("Complete County Name",'Riverside|San Bernardino') group by all order by 1,2,3""")
q("HRSA sites file", """select count(*) rows, max("Data Warehouse Record Create Date") dw from hc""")
fl = first("X_chhs_facility_locations/health_facility_locations.csv")
con.execute(f"create view fl as select * from read_csv('{fl}', all_varchar=true, header=true, null_padding=true, strict_mode=false)")
q("CHHS facility locations: IE counts by type", """select COUNTY_NAME, FAC_FDR, count(*) n from fl where upper(COUNTY_NAME) in ('RIVERSIDE','SAN BERNARDINO') group by all order by 3 desc""", 12)
ru = first("X_usda_ruca_zip/*.csv")
con.execute(f"create view ru as select * from read_csv('{ru}', all_varchar=true, header=true)")
q("RUCA primary codes for IE-touching ZCTAs", """select PrimaryRUCA, count(*) zips from ru where State='CA' and ZIPCode in (select z from ie_z) group by 1 order by 1""")
pl = first("X_cdc_places_zcta/*places_zcta.csv")
con.execute(f"create view pl as select * from read_csv('{pl}', all_varchar=true, header=true)")
q("PLACES rows / IE-touching ZCTAs present", "select count(*) rows, sum(case when ZCTA5 in (select z from ie_z) then 1 else 0 end) ie_zctas from pl")
for t in ("b01003", "b01001", "b17001", "c16001", "b08201", "b27001", "b19013"):
    f = first(f"X_acs5_zcta/acsdt5y*-{t}.dat")
    q(f"ACS {t}: rows, ZCTA rows, IE-touching ZCTAs present", f"""select count(*) rows, sum(case when GEO_ID like '860Z200US%' then 1 else 0 end) zcta_rows,
 sum(case when GEO_ID like '860Z200US%' and substr(GEO_ID,10) in (select z from ie_z) then 1 else 0 end) ie_zctas from read_csv('{f}', delim='|', all_varchar=true, header=true)""")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {OUT} ({len(lines)} lines)")
