# Data dictionary (real column names as downloaded)

Retrieved 2026-11-02. Raw files are in `data/raw/<source_key>/`, unchanged. Provenance and SHA-256 are in
`data/catalog/download_manifest.csv`; per-dataset facts are in `data/catalog/dataset_inventory.csv`;
counts quoted here come from `scripts/inspect_downloads.py` (output `data/catalog/inspection_summary.txt`).

Meanings come from the publishers' own field definitions where they exist (CKAN datastore field notes saved as
`_datastore_fields_<resource id>.json`, Socrata metadata JSON, Census table shells, HRSA/CHHS dictionaries). Where
a meaning is my reading of the data and not a publisher definition it is marked **[inferred]**.

Global read rules (every CSV):
- Read every column as text first (`all_varchar=true`). ZIP, ZCTA, NPI, FIPS and code columns have leading zeros.
- Counts are text with thousands separators in A, B, D (`"54,989"`, D also pads spaces: `" 293,311 "`). Strip `,` and spaces before casting.
- Blank / NULL counts with an Annotation Code are suppressed, not zero.
- A, B, D use `Annotation Code` 1 = suppressed small number, 2 = suppressed complementary cell (A also lists 3 = no data available, which does not occur). `Statewide Total by MOE` rows (Annotation Description) are statewide totals, not suppression.
- Encodings: E is **Latin-1/Windows-1252, not UTF-8** (`encoding='latin-1'`). D, F, H, E-code-refs have a UTF-8 BOM. D needs `header=true` (header has a trailing comma). G files have a header with one extra trailing empty column name; read with `null_padding=true`.

---------------------------------------------------------------------------------------------------

## A. `A_zip_eligibles_2020_recent/oct2026_productionsecondsheet_2020_recent.csv` (646,584 rows)

| Column | Meaning |
|---|---|
| `Month of Eligibility` | `YYYY-MM`. Month in which the beneficiary was certified eligible. 2020-01 to 2026-10; **2025-10 is absent**. |
| `Zip Code` | Beneficiary residential 5-digit ZIP, text, **padded with spaces in the file for the special rows**. Special values: `.` (invalid or out-of-state ZIP; 243 rows, space-padded) and `STATEWIDE` (81 rows, one per month and sex). |
| `Sex` | `Female`, `Male`, or `Total`. Total = Female + Male wherever all three are published (0 mismatches in IE ZCTAs, Sep 2026). |
| `Total Eligibles` | Count of certified eligibles (text with commas). Blank when suppressed. |
| `Annotation Code` | `1` suppressed small number (164,732 rows), `2` suppressed complementary cell (5,103 rows), blank otherwise. |
| `Annotation Description` | Text for the code, or `Statewide Total by MOE`. |
| `Status` | `F` final (months 2020-01 to 2025-09) or `P` preliminary (2025-11 to 2026-10). DHCS: a month is final 12 months after month end. |
| `Date of Data` | Snapshot date `DDMMMYYYY`. All `P` months are `07OCT2026`. |

There is **no county column**.

## B. Source B files (county level). Common columns

`Month of Eligibility` (`YYYY-MM`, 2010-01 to 2026-10, 2025-10 absent), `County` (name text; 58 counties plus the label `STATEWIDE`; 60 distinct labels), `Total Eligibles`, `Annotation Code`, `Annotation Description`, `Status` (F/P as in A), `Date of Data` (blank values appear as `        .`).

| File | Extra columns / values |
|---|---|
| `B_age_sex/t1_eligibility_by_age_group_sex_201001_oct2026.csv` (93,469 rows) | `Age Group`: `Age 00-18`, `Age 19-44`, `Age 45-64`, `Age 65+`, `STATEWIDE`; `Gender`: `Female`, `Male`, `STATEWIDE`. |
| `B_language/t5_eligibility_by_language_201001_oct2026.csv` (252,912 rows) | `Language` (34 labels incl. English, Spanish, Mandarin, Vietnamese, Arabic, `Missing/Unknown`, ` Unknown` with leading space, `Other Non-Eng`, `ASL`, `STATEWIDE`); `Difference` (entirely empty column). |
| `B_delivery_plan/t2_eligibility_by_delivery_system_plan_201001_oct2026.csv` (49,920 rows) | `Health Delivery System`: `Fee-for-Service`, `Managed Care`, `STATEWIDE`; `Health Plan` (275 labels such as `Inland Empire Health Plan/Riverside`, `Molina Healthcare of California/San Bernardino`, `Out of County Plan`, `Fee-for-Service`). |
| `B_race_ethnicity/t4_eligibility_by_race_ethnicity_age_group_201001_oct2026.csv` (277,204 rows) | `Age Group` as above; `Ethnicity`: `AI/AN`, `ASIAN`, `BLACK`, `HISPANIC`, `WHITE`, `NOT REPORTED`, `STATEWIDE`. |

Not downloaded by policy: By Aid Category (and the bundle ZIP containing it).

## C. `C_iehp_factsheet/IEHP_Fact_Sheet.pdf`
Single page PDF, text extractable. Values (October 2026, count month not stated): Medi-Cal 1,321,983; IEHP DualChoice Medicare-Medicaid Plan 38,185; IEHP Covered (Covered California) 34,078; total 1,394,246. Provider network: PCP 1,488; Specialists 2,817; Behavioral Health 3,453; Hospitals 34; Other (vision, therapist, midlevel, mobile PCP, no assignment PCP, urgent care) 2,570; total 10,362. Text states IEHP serves "more than 90% of the Medi-Cal managed care market" in the region.

## D. `D_managed_care_enrollment/open-data-portal-managed-care-enrollment-count-september-2026.csv` (31,771 rows)

| Column | Meaning |
|---|---|
| `Enrollment Month` | `YYYY-MM`, 2007-01 to 2026-09. |
| `Plan Type` | 20 labels, e.g. `Local Initiative (2 Plan)` (IEHP), `Commercial Plan (2 Plan)` (Molina, Kaiser in the IE), `PACE`, `SCAN`, `COHS`, `Dental`, `Geographic Managed Care`. |
| `County` | County name. |
| `Plan Name` | Plan label with county suffix, e.g. `Inland Empire Health Plan/Riverside`. **SCAN Health Plan appears twice per county with the same name** (different lines of business, not distinguishable in the file) [inferred]. |
| ` Count of Enrollees ` | Enrollment count, text with spaces and commas (column name itself has leading and trailing spaces). |
| `Count of Enrollees Annotation Code` | `1`, `2`, or the literal string `None`. |
| `Count of Enrollees Annotation Description` | Text or literal `None`. |
| (8th, unnamed) | Always empty; produced by a trailing comma. |

## E. `E_ffs_providers/medi-cal-ffs-provider-listing_10_26_26.csv` (380,888 rows; 51 columns)
Publisher definitions are in `_datastore_fields_d652b210-...json`.

| Column | Meaning |
|---|---|
| `Provider_Number` | DHCS identifier; holds NPI and legacy number. Equals `NPI` on every IE row. 310,086 distinct statewide. |
| `NPI` | National Provider Identifier (text, 10 digits). 310,037 distinct vs 380,888 rows. Blank/0 in 2 IE rows. |
| `NPI_Type` | `Type 1` individual, `Type 2` organization; 49 blank. |
| `Owner_Number`, `Service_Location_Number` | Owner sequence number and service location number within the provider. |
| `Legal_Name` | Provider name (personal data; counts only). |
| `Enroll_Status_Eff_DT` | Enrollment status effective date, text `M/D/YYYY 0:00`; ranges 1966-01 to 2026-10-15. |
| `Provider_Taxonomy` | NUCC taxonomy code, or `No Taxonomy Provided` (10,469 IE rows). |
| `NEMT_NMT_Provider_Type`, `ANC_Provider_Type` | Transportation mode; mapped network-certification type (e.g. `Adult Primary Care`, `Mental Health Outpatient Services`, `Pediatric Primary Care`, `Other`). ANC type is blank or `N/A` for 18,910 IE rows. |
| `FI_Provider_Type_CD`, `FI_Provider_Type` | 3-character type code and description (`026` PHYSICIANS, `035` RURAL HEALTH CLINICS/FEDERALLY QUALIFIED HEALTH CENTER, `041` COMMUNITY CLINIC, `096` TRIBAL FQHC PROVIDERS, `077` MFT individual, `070` LCSW individual, `007` CERTIFIED NURSE PRACTIONER [sic]). Lookup in `provider-type-code-reference_2.2026.csv`. Value `N/A` or `000/Unknown` for Provider_Source 2/3 rows. |
| `Provider_License` | CA license number, only for types 026, 086, 087; `-` or blank otherwise. |
| `FI_Provider_Specialty_CD`, `FI_Provider_Specialty` | Principal specialty (required only for physician groups, physicians, NPs, midwives, nurse anesthetists, EPSDT, podiatrists, PTs, psychologists). Blank, `-` or `N/A` otherwise. E.g. `08` Family Practice, `41` Internal Medicine, `40` Pediatrics, `01` General Practice, `36` Psychiatry, `66` Emergency Medicine (Urgent Care). |
| `Out_of_State_Indicator`, `In_Out_State` | 0 in state, 1 border, 2 out of state, 3 out of country, 4 out of state EDS; description. `N/A` for Provider_Source 3. |
| `Address_Attention`, `Address`, `Address2`, `City`, `State`, `ZIP`, `ZIP_4` | Service location. `ZIP` 5 digits. 278 rows with `County` = Riverside or San Bernardino have `State`, `City`, `ZIP` and `Address` all equal to the string `N/A` (enrolled, no service address; excluded from the 36,470-row IE definition, which requires `State`='CA'). |
| `DHCS_County_CD`, `FIPS_County_CD` | County codes where service is provided. **FIPS_County_CD is inconsistent** with the county name (e.g. `06000` on 8,428 IE rows, 06037 on Riverside rows). Do not trust. |
| `County` | County name from the provider file. **`N/A` for 94,409 rows** (all Provider_Source 2 and 3), `UNKNOWN` for 7,975. |
| `Phone_Number`, `Provider_Website`, `Threshold_Languages`, `Other_Languages` | Contact and languages (mostly blank). |
| `Medicaid_Patients` | "Is the provider currently accepting new Medicaid patients?" `N` not accepting; `F` FFS patients only; `M` managed care only; `B` both. **Populated on only 18,501 rows statewide (4.9%)**, 1,614 of 36,470 IE rows. |
| `CHIP_Patients` | `Y`/`N` accepting new CHIP patients (same sparse coverage). |
| `Telehealth_Services` | `Y`/`N`. |
| `Acc_Exam_Room`, `Acc_Exterior_Building`, `Acc_Interior_Building`, `Acc_Parking`, `Acc_Restroom`, `Acc_Medical_Equipment`, `Acc_Patient_Areas`, `Acc_Patient_Diagnostic` | `Y`/`N` accessibility accommodations (same sparse coverage). |
| `Provider_Source` | DHCS internal: `1` Main File (286,479 rows), `2` NMP File (26,130), `3` ORP File (68,279). Expansion of NMP/ORP is not given [UNVERIFIED]. Source 3 rows are all non-billing, have no type, no county, no state. |
| `Billing_Provider` | `FFS Billing Provider`: actively enrolled and bills Medi-Cal under its own NPI. `FFS Non-Billing Provider`: actively enrolled individual who renders services but does not submit claims directly (publisher definition). 99,090 billing rows statewide. |
| `Latitude`, `Longitude` | Coordinates (0 blank in IE). |
| `CountyName` | "County based off Latitude and Longitude Coordinates", form `Riverside County`. Blank on a handful of rows. More reliable than `County` for IE membership. |

Row grain: one row per provider number x service location. One person can appear at several addresses and under several provider types. 27,012 of 30,520 IE NPIs have one row; the rest repeat (up to 10+ rows).

`E_ffs_providers/provider-type-code-reference_2.2026.csv`: `Provider Type Code (r)`, `Provider Type Desc (r)` (108 rows; BOM in first header). `provider-specialty-code-reference_2.2026.csv`: specialty code and description (65 rows). Codes are zero-padded text.

## F. `F_dental_ffs_providers/ffsproviderprofileodp_oct2025.csv` (53,303 rows)

`Provider NPI`, `Billing Provider Number`, `Service Location Number`, `Provider Legal Name`, `Enrollment Status Effective Date` (`21-Jan-92` style, often blank), `Provider Type Code` (`R` Dental Rendering, `B` Dental Billing, `RC` Rendering Provider at Safety Net Clinic, `C` Safety Net Clinic), `Provider Type Code Desc`, `Provider Specialty Code`, `Provider Specialty Code Desc` (e.g. General Practitioner (Dentists Only), Pedodontist, Certified Orthodontist, Oral Surgeon), `Provider Language Code`, `Provider Language Code Desc`, `Provider County Code`, `Provider County Desc` (5,394 blank), `Billing Provider Address Attention Line`, `Billing Provider Address 1`, `Billing Provider Address 2`, `Billing Provider City`, `Billing Provider State`, `Billing Provider Zip`, `Latitude`, `Longitude`, `MSSA ID`, `Tract ID`.
`ffs_dental_provider_count_dec2025.csv`: `Month/Year` (July 2016 to June 2025), `Rendering Providers`, `Active Service Offices`, `Safety Net Clinics` (quoted comma counts).

## G. HRSA HPSA files (`BCD_HPSA_FCT_DET_PC.csv`, `_MH.csv`, `_DH.csv`)
65 data columns (PC has a 66th header name, `PC MCTA Score`, that MH/DH lack). Key columns:

| Column | Meaning |
|---|---|
| `HPSA Name`, `HPSA ID` | Designation name and id (one HPSA ID spans many component rows). |
| `Designation Type` | e.g. `Geographic HPSA`, `HPSA Population`, `High Needs Geographic HPSA`, `Federally Qualified Health Center`, `Federally Qualified Health Center Look A Like`, `Rural Health Clinic`, `Correctional Facility`, `Indian Health Service, Tribal Health, and Urban Indian Health Organizations`, `Other Facility`. |
| `HPSA Discipline Class` | `Primary Care` / `Mental Health` / `Dental Health`. |
| `HPSA Score` | Need score; observed IE Designated ranges PC 6-19, MH 3-22, DH 8-25. 0 appears on withdrawn rows. |
| `HPSA Status` | `Designated`, `Proposed For Withdrawal`, `Withdrawn`. Filter before use. |
| `HPSA Designation Date`, `HPSA Designation Last Update Date`, `Withdrawn Date` | Dates `MM/DD/YYYY`. |
| `HPSA Geography Identification Number` | County FIPS (5 digits), census tract GEOID (11 digits) or the literal `POINT` for facility designations. |
| `HPSA FTE`, `HPSA Designation Population`, `HPSA Formal Ratio`, `HPSA Estimated Underserved Population`, `HPSA Shortage`, `HPSA Provider Ratio Goal` | Shortage arithmetic (FTE short, population, ratios like `8938:1`). |
| `Common County Name` | Form `Riverside County, CA`. Also `County Equivalent Name`, `Common State County FIPS Code`, `State and County Federal Information Processing Standard Code`. |
| `HPSA Postal Code`, `HPSA Address`, `HPSA City` | Present for facility POINT rows; blank for most area-based rows (e.g. 234 of 261 PC Designated IE rows). |
| `Longitude`, `Latitude`, `Rural Status`, `Metropolitan Indicator` | Location and rural flags. |
| `Data Warehouse Record Create Date`, `Data Warehouse Record Create Date Text` | Extract date (2026/11/02). |

## H. `H_census_zcta_county/tab20_zcta520_county20_natl.txt` (pipe-delimited, 47,863 rows)
`OID_ZCTA5_20`, `GEOID_ZCTA5_20` (5-digit ZCTA, blank on rows for county area with no ZCTA), `NAMELSAD_ZCTA5_20`, `AREALAND_ZCTA5_20`, `AREAWATER_ZCTA5_20`, `MTFCC_ZCTA5_20`, `CLASSFP_ZCTA5_20`, `FUNCSTAT_ZCTA5_20`, `OID_COUNTY_20`, `GEOID_COUNTY_20` (5-digit county FIPS), `NAMELSAD_COUNTY_20`, `AREALAND_COUNTY_20`, `AREAWATER_COUNTY_20`, `MTFCC_COUNTY_20`, `CLASSFP_COUNTY_20`, `FUNCSTAT_COUNTY_20`, `AREALAND_PART`, `AREAWATER_PART` (square meters of the intersection). No population or address weights.
HUD crosswalk: blocked, see report.

## X. Additional sources

**X_tiger_zcta_2020** (`cb_2020_us_zcta520_500k.zip`): `ZCTA5CE20`, `AFFGEOID20`, `GEOID20`, `NAME20`, `LSAD20`, `ALAND20`, `AWATER20`, `geometry` (EPSG:4269), 33,791 polygons.
**X_tiger_county_2020** (`cb_2020_us_county_500k.zip`): `STATEFP`, `COUNTYFP`, `COUNTYNS`, `AFFGEOID`, `GEOID`, `NAME`, `NAMELSAD`, `STUSPS`, `STATE_NAME`, `LSAD`, `ALAND`, `AWATER`, `geometry`; 3,234 rows.

**X_acs5_zcta** (`acsdt5y2024-<table>.dat`, pipe-delimited, one row per geography): `GEO_ID` (ZCTA rows are `860Z200US#####`; ZCTA = `substr(GEO_ID,10)`), then for each table cell `<TABLE>_E###` (estimate) and `<TABLE>_M###` (margin of error). Meanings come from `ACS2024_ACS20245YR_Table_Shells.txt` (columns `Table ID|Line|Indent|Unique ID|Label|Title|Universe|Type`); `ACS2024_Geos20245YR.txt` has `GEO_ID`, `NAME`, `ZCTA5`, etc. Tables:
- `B01003_E001` total population; `B01001` sex by age (`_E002` male total ... ); `B17001_E001` poverty universe, `_E002` below poverty level; `C16001_E001` population 5+ speaking, `_E002` English only, `_E003` Spanish, `_E005` Spanish and speaks English less than "very well", analogous triples for French/German/Slavic/Other Indo-European/Korean/Chinese/Vietnamese/Tagalog/Other Asian-Pacific/Arabic/Other; `B08201_E001` households, `_E002` no vehicle available; `B27001_E001` civilian noninstitutionalized population, `_E005`/`_E008` etc. are "No health insurance coverage" cells by sex and age band (see shells); `B19013_E001` median household income (2024 dollars).
- Sentinels: estimate `-666666666` = no estimate (370 CA ZCTAs on median income); margin `-222222222` and `-555555555` = not computable / not applicable. Treat as missing, not as numbers.
- No citizenship, nativity or foreign-born tables were downloaded.

**X_cdc_places_zcta** (`kee5-23sr_places_zcta.csv`, 32,520 rows): `ZCTA5`, `TotalPopulation` (Census 2020), `TotalPop18plus`, then for 40 measures `<MEASURE>_CrudePrev` (percent) and `<MEASURE>_Crude95CI` (text like `( 3.8,  5.3)`), `Geolocation` (`POINT (lon lat)`). Measures include `ACCESS2` (adults 18-64 lacking health insurance, 2023), `CHECKUP` (routine checkup in past year; "no routine checkup" = 100 - CHECKUP), `DENTAL` (dentist visit, 2022), `DIABETES`, `DEPRESSION`, `MHLTH`, `PHLTH`, `LACKTRPT` (lack of reliable transportation), `FOODSTAMP`, `FOODINSECU`, `HOUSINSECU`, `DISABILITY`, `OBESITY`, `BPHIGH`, `CASTHMA`, `COPD`, `CSMOKING`, `GHLTH`, and others. Descriptions: `kee5-23sr_metadata.json` `columns[].description`. No year column; BRFSS 2023 for most measures, 2022 for dental, teeth lost, mammography, colorectal screening, short sleep.

**X_hrsa_health_center_sites** (`Health_Center_Service_Delivery_and_LookAlike_Sites.csv`, 19,514 rows, 55 columns): key columns `Health Center Type`, `Health Center Number`, `BPHC Assigned Number`, `Site Name`, `Site Address`, `Site City`, `Site State Abbreviation`, `Site Postal Code`, `Operating Hours per Week`, `Health Center Service Delivery Site Location Setting Description`, `Site Status Description` (all `Active`), `FQHC Site NPI Number`, `Health Center Location Type Description` (`Administrative`, `Service Delivery Site`, `Administrative/Service Delivery Site`), `Health Center Type Description`, `Health Center Name`, `Geocoding Artifact Address Primary X Coordinate` (longitude), `...Y Coordinate` (latitude), `State and County Federal Information Processing Standard Code`, `Complete County Name`, `Data Warehouse Record Create Date`, plus a stray last column `column55`.

**X_chhs_facility_locations** (`health_facility_locations.csv`, 14,921 rows): `FACID`, `FACNAME`, `FAC_TYPE_CODE`, `FAC_FDR` (type roll-up, e.g. `PRIMARY CARE CLINIC`, `GENERAL ACUTE CARE HOSPITAL`, `CHRONIC DIALYSIS CLINIC`), `LICENSED_CERTIFIED`, `T18_19` (Medicare/Medi-Cal certification), `CCN`, `NPI`, `CAPACITY` (licensed beds), `ADDRESS`, `CITY`, `ZIP`, `ZIP9`, `COUNTY_CODE`, `COUNTY_NAME`, `FIPS_COUNTY_CODE`, `LICENSE_STATUS_DESCRIPTION`, `LICENSE_NUMBER`, `ENTITY_TYPE_DESCRIPTION`, `LATITUDE`, `LONGITUDE`, `HCAI_ID`, `TYPE_OF_CARE`, `DATA_DATE`, and administrator/contact fields (not used). Full definitions: `datadictionary_facilities_rev20250115.xlsx`; lookups: `lookup-table_facilities_rev20250115.xlsx`.

**X_usda_ruca_zip** (`2020-rural-urban-commuting-area-codes-zip-codes.csv`, 41,146 rows): `ZIPCode` (text), `State`, `ZIPCodeType` (`ZIP Code Area` or `Post Office or large volume customer`), `POName`, `PrimaryRUCA` (1-10; 10 = rural), `SecondaryRUCA` (e.g. `10.1`). IE ZIPs: primary codes 1 (104), 2 (15), 3 (5), 4 (15), 5 (3), 6 (1), 7 (7), 10 (18).

## Join keys at a glance
| From | To | Key and caution |
|---|---|---|
| A | ACS / PLACES / TIGER / rel2020 | A `Zip Code` is a postal ZIP. Others are ZCTA. Join on the 5-character text and flag ZIPs with no ZCTA (e.g. PO boxes). 168 of 169 IE-touching ZCTAs are in A for 2026-09 (the missing one, 89019, is in Nevada). |
| A / E / F | county | Use rel2020 (`GEOID_ZCTA5_20`, `GEOID_COUNTY_20`, `AREALAND_PART`) for A. For E use `CountyName` (and ZIP) not `County`. For F use `Provider County Desc` and ZIP. |
| E | F | Both carry NPI; E is medical, F is dental FFS. |
| B | D | County name text; plan names differ between B (`Health Plan`) and D (`Plan Name`) in counts. |
