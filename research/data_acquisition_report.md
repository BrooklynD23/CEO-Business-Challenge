# Data acquisition report (Phase 0)

Retrieved 2026-11-02 (UTC) by `scripts/download_data.py`. Profiled by `scripts/inspect_downloads.py`
(full output: `data/catalog/inspection_summary.txt`). Catalog files: `data/catalog/download_manifest.csv`
(url, retrieved_at, sha256, bytes, status, blocker, plus local_path and note), `data/catalog/dataset_inventory.csv`,
`data/catalog/data_dictionary.md`. Raw files: `data/raw/<source_key>/`, unchanged since download.

Evidence labels: `[VERIFIED: source, 2026-11-02]` = read from the downloaded source; `[COMPUTED: scripts/inspect_downloads.py]`
= counted from raw files; `[UNVERIFIED]` = could not establish. No correlation analysis was done.

## 1. What was obtained

| Key | What | Status |
|---|---|---|
| A | Medi-Cal certified eligibles by ZIP and sex, "Calendar Years 2020 to the Most Recent Reportable Month" only (31.5 MB, 646,584 rows) | ok |
| B | By Age Group and Sex, By Primary Language, By Delivery System and Plan, By Race/Ethnicity and Age Group (county level) | ok |
| B (excluded) | By Aid Category | **Not downloaded, not opened.** Manifest row `B_by_aid_category` = `excluded_by_policy`. The "All resource data" ZIP for B was also not fetched because it bundles that file. A guard in `pick_b_resources` aborts if a matching resource is ever selected. |
| C | IEHP Fact Sheet PDF (Oct 2026, 1 page) | ok, text extracted |
| D | Medi-Cal managed care enrollment, September 2026 file (2007-01 to 2026-09) | ok |
| E | Medi-Cal FFS provider list (as of 2026-10-26, 120 MB, 380,888 rows) + provider type and specialty code references | ok |
| F | Dental FFS providers and safety net clinics (as of Oct 2025) + monthly count file | ok (stale) |
| G | HRSA HPSA primary care, mental health, dental (`BCD_HPSA_FCT_DET_PC/MH/DH.csv`, data warehouse date 2026-11-02) | ok |
| H | HUD ZIP-County crosswalk | **BLOCKED** (account registration required; not registered). Substitute `H_census_zcta_county` downloaded. |
| X | Census 2020 cartographic ZCTA and county boundaries; ACS 2020-2024 5-year ZCTA tables (7 tables); CDC PLACES ZCTA 2025 release; HRSA health center sites; CHHS licensed facility locations; USDA 2020 RUCA by ZIP | ok |
| X | CMS NPPES | **Feasibility only, not downloaded; bulk file not confirmed** (see 3) |

Re-running `download_data.py` is idempotent: existing files are reported as `cached` and nothing is overwritten
(a changed remote file would be saved beside the original with a date suffix). An early bug (section 3) re-downloaded six files
and the copies came out byte-identical to the originals (SHA-256 equal), which doubles as a reproducibility check.

## 2. Answers to the critical checks

**Do A and E carry a county column?**
- **A: no.** Columns are Month of Eligibility, Zip Code, Sex, Total Eligibles, Annotation Code, Annotation Description, Status, Date of Data. County must come from a crosswalk. [VERIFIED: A header]
- **E: yes, but unreliable.** Three county-ish fields: `County` (name from the provider file), `CountyName` (derived from latitude/longitude, per publisher), and `FIPS_County_CD`. `County` is `N/A` on 94,409 rows (all Provider_Source 2 and 3), including 8,428 rows whose `CountyName` is Riverside or San Bernardino (23% of the IE rows). `FIPS_County_CD` is wrong or `06000` on those same rows. Filtering on `County` alone silently drops about 8,400 IE rows. Use `State='CA'` and (`County` in the two counties or `CountyName` in `Riverside County`, `San Bernardino County`). That gives 36,470 rows (Riverside + San Bernardino combined), 36,207 of them in a ZIP that sits in an IE-touching ZCTA. [COMPUTED]

**Does A's latest month include Aug or Sep 2026?** Yes, and more. A runs 2020-01 to **2026-10**: 81 months, because **2025-10 is missing**. August, September and October 2026 are all present, all `Status = P` (preliminary), all snapshot-dated `07OCT2026`. Per the publisher, a month is final 12 months after month end, so the **latest final month is 2025-09**. The guide's "use Aug or Sep 2026" means using preliminary data. Statewide totals fall steadily (Sep 2026 13,380,286; Oct 2026 13,089,574, a one-month drop of 2.2%); October was captured on the 7th and is most likely incomplete. Recommend the analyst use 2026-09 as the main month, 2026-08 as a sensitivity, and show 2025-09 (final) as a check. B shows the same pattern: Riverside FFS 59,847 (Aug), 52,453 (Sep), 35,046 (Oct). [COMPUTED]

**Are FQHCs/clinics visible as provider types in E?** Yes. IE rows (rows / unique NPI): `035` RURAL HEALTH CLINICS/FEDERALLY QUALIFIED HEALTH CENTER 168/109; `041` COMMUNITY CLINIC 66/25; `045` CLINIC EXEMPT FROM LICENSURE 24/17; `048` COUNTY CLINICS 4/4; `096` TRIBAL FQHC PROVIDERS 9/9; `075` INDIAN HEALTH SERVICES 3/3. FQHC and RHC are one combined code (035), so FQHC cannot be separated from rural health clinics using E alone. HRSA site data (`X_hrsa_health_center_sites`: Riverside 116 and San Bernardino 62 service delivery sites, plus 12 combined administrative/service-delivery sites) is the better FQHC source. Clinic records are billing entities (all 271 rows are billing providers). Physicians who work in clinics appear separately, so clinic and practitioner rows must not be summed. [COMPUTED]

**Do provider rows have an NPI that identifies duplicates?** Yes. `NPI` is present on every IE row (2 blank/0), and `Provider_Number` equals NPI on all IE rows. Rows are provider-number x service-location, not people. IE: **36,470 rows, 30,520 unique NPIs, 32,529 unique NPI-address-ZIP combinations**. 27,012 NPIs appear once; 2,918 twice; 323 three times; some 10+ times. 1,109 NPIs appear in more than one county label. Statewide: 380,888 rows, 310,037 NPIs. Type 2 (organization) and Type 1 (individual) share the table; an individual may also appear under a group. Dedupe on NPI for "unique practitioners" only after choosing provider types, and count NPI-ZIP pairs for ZIP-level supply (an NPI at two ZIPs legitimately counts in both). [COMPUTED]

**Anything on active billing vs mere enrollment, or new-patient acceptance?**
- `Billing_Provider`: `FFS Billing Provider` (actively enrolled, bills under its own NPI) vs `FFS Non-Billing Provider` (enrolled individual who renders services but does not submit claims directly). It is a role flag, not claims volume or recent activity. IE: 10,497 billing rows (6,708 NPIs), 25,973 non-billing rows. Non-billing individuals often bill through a group, so excluding them undercounts practitioners and including them double counts capacity with the group row. [VERIFIED: publisher field definition]
- `Provider_Source` (`1` Main, `2` NMP, `3` ORP file; DHCS "internal use only"): Source 3 rows (5,035 in IE) are all non-billing, with no provider type, no county and no state; expansion of "ORP" is not given [UNVERIFIED] (it may mean ordering/referring/prescribing providers, who typically cannot bill). Source 2 rows (3,393 in IE) also have no type. Together 4,754 IE rows (13%) cannot be assigned a provider type. Excluding Source 3 leaves 31,435 rows / 26,391 NPIs.
- `Medicaid_Patients` is exactly the "currently accepting new Medicaid patients?" flag (`N` no; `F` FFS only; `M` managed care only; `B` both), but it is populated on only **18,501 of 380,888 rows (4.9%)** statewide, and 1,614 of 36,470 IE rows (B 1,283; N 137; F 118; M 76). It exists almost only on billing rows from Source 1. The guide's statement that new-patient acceptance is not observable is therefore nearly right: a partial, self-reported flag exists but is too sparse to build a ratio on. Treat it as a sensitivity check for the minority of records that have it. CHIP acceptance and telehealth flags have the same sparse coverage.
- `Enroll_Status_Eff_DT` is the enrollment effective date (latest 2026-10-15, 1,931 IE rows effective in 2026). No last-claim date or claims counts exist.

## 3. Blockers and failures

| Item | What happened | Handling |
|---|---|---|
| HUD ZIP-County crosswalk (H) | Needs an account. Not registered, per contract. | Manifest `blocked`. Used Census 2020 ZCTA-county relationship file (area based) plus county in E/F. |
| Census API (ACS) | The keyless API now answers HTTP 302 to "Missing Key" (a key requires an email sign-up). | Used the keyless bulk ACS **table-based summary file** from www2.census.gov instead (same estimates and margins, but whole-nation files: 18-200 MB each). Vintage 2020-2024, the newest present. |
| CMS NPPES | download.cms.gov page says "site will be down for maintenance until further notice", lists no zip, and guessed monthly file names return 404. The keyless per-query NPI Registry API (npiregistry.cms.hhs.gov) answers. | Manifest `bulk_file_not_confirmed`; nothing downloaded; no provider records stored. |
| HRSA HEAD request, Socrata HEAD request | A gzip HEAD reported 20 or 0 bytes, which made my first size check re-download six files into byte-identical `*.retrieved20261102.*` copies. Script fixed (identity encoding, ignore tiny sizes). | The six duplicate files remain on disk because the rule forbids deleting raw files; they are listed in section 6. Safe to delete on your instruction. |

No source failed outright. No account, key or credential was used.

## 4. Surprises

1. A and every B file skip **2025-10**. A series built on a contiguous month index will break there.
2. The guide's recommended months (Aug/Sep 2026) are preliminary. Latest final is 2025-09.
3. **Three different IEHP Medi-Cal counts:** fact sheet 1,321,983 (Medi-Cal only; with DualChoice 1,360,168); D, Sep 2026, 677,919 + 685,384 = 1,363,303; B delivery-plan table, Sep 2026, 668,559 + 671,883 = 1,340,442. County totals of all eligibles in B Sep 2026: Riverside 912,055 (FFS 52,453 + managed care 859,602), San Bernardino 905,173 (FFS 46,753 + managed care 858,420). D managed care Sep 2026 (non-dental): Riverside 859,149; San Bernardino 866,080. [COMPUTED]
4. E: `County` and `FIPS_County_CD` are unreliable (above). The file is Latin-1, not UTF-8; reading as UTF-8 fails at line 80,028.
5. E has no FQHC-only type, a quasi new-patient flag, and a billing flag; none of them is capacity.
6. Format traps: D has a UTF-8 BOM, space-padded counts, a duplicate-named SCAN row per county, and `None` strings; G has a header with one extra name; A's special ZIP rows `.` and `STATEWIDE` are space-padded; B Language has `Unknown` with a leading space; HRSA sites has a stray `column55`.
7. F (dental) is as of Oct 2025 (13 months old) and has 5,394 rows with blank county; the monthly count file stops at June 2025 despite the "dec2025" file name.
8. PLACES `CHECKUP_CrudePrev` is the share who **had** a checkup. "No routine checkup" is 100 minus that. `ACCESS2` is lack of health insurance (adults 18-64), not access to care.

## 5. Specifics the analyst must know

**Geography.** ZIP (A, E, F, RUCA) is not ZCTA (ACS, PLACES, TIGER, rel2020). Store both as 5-char text in separate columns `zip` and `zcta`. 169 ZCTAs touch Riverside (06065) or San Bernardino (06071); 168 of them appear in A for 2026-09 (the missing one is 89019, which is mostly Nevada). 19 of the 169 span more than one county (pairs include 91759, 92277, 92397, 92399); 162 have a majority of land area in the two counties and 7 do not. The rel2020 file gives only land and water area overlap (`AREALAND_PART`), so area-majority assignment can differ from where people live (92277 is 78% San Bernardino by land area, 3,230 vs 912 sq km, which says nothing about where its residents live). Choose and document one rule (for example majority land area with a flag for split ZCTAs). A's IE-touching ZCTA total for 2026-09 is 1,871,886 vs 1,817,228 from B county totals, so the ZIP route overshoots by about 3% because split ZCTAs include out-of-county residents.

**Suppression.** In A, IE ZCTAs in 2026-09: 5 suppressed Total cells (code 1), none code 2 for Total (code 2 appears only on three Male cells). Never fill with zero. B Language is heavily suppressed for small languages (94,805 suppressed cells overall). B Age/Sex has 174. ACS uses sentinel negative numbers (`-666666666`). PLACES has no suppression but covers only 162 of 169 IE-touching ZCTAs.

**Denominators.** A and B count ALL Medi-Cal certified eligibles (managed care + FFS + other plans, including Molina, Kaiser, PACE). D counts managed care enrollees by plan. The fact sheet counts IEHP Medi-Cal only. E counts FFS-enrolled provider records (not people). Label each ratio. FFS "existing members" are only 52,453 (Riverside) and 46,753 (San Bernardino) in B.

**Supply definitions to settle before counting.** Primary care in E needs a rule on type (026 physicians with specialty 08 Family Practice, 41 Internal Medicine, 40 Pediatrics, 01 General Practice; 007/010 nurse practitioners; clinic types 035/041/048). Illustrative scale only: IE rows with physician specialties 08/41/40/01 are 4,725 rows (4,527 NPIs). 2,116 IE physician rows have a blank specialty code and 860 have `N/A`. Mental health: types 077, 070, 031, 103 and psychiatry (specialty 36); `ANC_Provider_Type` = `Mental Health Outpatient Services` (3,618 IE rows) is a mapped alternative. Dental comes only from F. Reminder: group (22/023/071/078/104) and individual rows overlap.

**HPSA.** Filter `HPSA Status = Designated`. Use `HPSA ID` for counting, because one designation has many component rows. Area-based designations carry county FIPS or tract GEOID in `HPSA Geography Identification Number`, not a ZIP (ZIP blank on 234 of 261 PC rows in IE). The guide is right: it cannot be assigned to ZIPs without a tract-to-ZCTA step.

**Sensitive-population compliance.** Nothing downloaded or derived estimates immigration status or UIS location. Aid Category file not obtained. ACS tables obtained: B01003, B01001, B17001, C16001, B08201, B27001, B19013; no citizenship, nativity, foreign-born or place-of-birth tables. Caution: C16001 (limited English proficiency by language), B race/ethnicity, and ZIP-level Medi-Cal counts could be misused as proxies for UIS; any sub-county use of them as demand allocation is an owner decision at the gate. I did not build any such proxy. I did read the CKAN metadata listing for dataset B, which names the Aid Category resource and its URL, but did not request that URL.

**Provider-level data.** E and F contain names, addresses and phone numbers of individual practitioners. Per contract they are for counting; no provider-level lists are reproduced in this report or the catalog.

## 6. Files and reproduction

- Run: `$HOME/.venvs/iehp-access/bin/python -I scripts/download_data.py [--only A B ...] [--force]`; profile with `... -I scripts/inspect_downloads.py`.
- CKAN metadata snapshots (`_ckan_package_show.json`) and datastore field definitions (`_datastore_fields_*.json`) are saved with each CHHS dataset and are rewritten on each run (they are metadata, not source data).
- Duplicate byte-identical copies from the early run (to be removed only on your instruction): `data/raw/G_hpsa_primary_care/BCD_HPSA_FCT_DET_PC.retrieved20261102.csv`, `data/raw/G_hpsa_mental_health/BCD_HPSA_FCT_DET_MH.retrieved20261102.csv`, `data/raw/G_hpsa_dental/BCD_HPSA_FCT_DET_DH.retrieved20261102.csv`, `data/raw/X_cdc_places_zcta/kee5-23sr_places_zcta.retrieved20261102.csv`, `data/raw/X_cdc_places_zcta/kee5-23sr_metadata.retrieved20261102.json`, `data/raw/X_hrsa_health_center_sites/Health_Center_Service_Delivery_and_LookAlike_Sites.retrieved20261102.csv`. The manifest points to the original files.
- Total raw size about 1.3 GB including the six duplicates (the ACS national files are about 0.6 GB of that).
- Licenses: CHHS CKAN metadata gives no `license_id`; PLACES is Public Domain per its metadata; federal files are public data; no license text was verified beyond that [UNVERIFIED].

## 7. Not established

- Whether the October 2026 A/B counts are incomplete (inferred from the sharp drop and the 7 October snapshot, not stated by DHCS).
- What the E `Provider_Source` values 2 and 3 stand for beyond "NMP File" and "ORP File".
- The count month of the IEHP fact sheet and how it treats duals (D vs fact sheet gap of about 3,100 is consistent with duals but not confirmed).
- HRSA and CHHS license terms; ACS release date (the HTTP header says 2026-01-29).
- New-patient acceptance for any provider other than the 4.4% of IE rows that carry the flag.
