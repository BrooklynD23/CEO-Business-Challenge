# Source register (policy workstream)

Retrieved 2026-11-02 unless stated. Source IDs are cited throughout `research/policy_verification.md`.

## How to read this table
- **Route** shows how the document was actually read.
  - `direct`: fetched from the publisher.
  - `archive`: read from a public Internet Archive snapshot of the publisher's URL (snapshot date given), because the publisher's site blocked automated access.
  - `host copy`: a copy of a DHCS document published by a Medi-Cal plan.
- **Reliability** is High for a primary document read in full, Medium for a secondary or dated source, Low for an unattributed or marketing-style source.

## Access limits
- `www.dhcs.ca.gov` returns an Incapsula bot wall to curl and returns empty pages to WebFetch. `www.census.gov`, `leginfo.legislature.ca.gov` and `ecfr.gov` also refused automated access.
- These walls were not solved or defeated. The first curl attempts sent a generic browser User-Agent string and were blocked anyway. Later requests used the default client.
- Documents were read through archive snapshots or plan-hosted copies where those existed. Every archive read is marked, so a human should re-open the live page before quoting it in the final deliverable.
- Section D lists documents known only through search-index excerpts. Nothing in them should be treated as verified.

## A. Primary: state and federal documents read in full

| ID | Document and URL | Publisher | Doc date | Route | Supports | Reliability |
|---|---|---|---|---|---|---|
| S01 | Policy Guide for Transition of the UIS Population, v3.0: https://www.cencalhealth.org/wp-content/uploads/2026/10/Version-3.0-DHCS-Policy-Guide-for-Transition-of-Members-with-an-Unsatisfactory-Immigration-Status-UIS-from-a-Managed-Care-Plan.pdf | DHCS | 2026-10-14 | host copy (CenCal) | Controlling document: population, carve-outs, continuity of care, data sharing, MCP duties, billing, duals, notices | High |
| S02 | Policy Guide v2.0: https://www.cencalhealth.org/wp-content/uploads/2026/09/version-2.0-of-the-DHCS-Policy-Guide-for-Transition-of-Members-with-an-Unsatisfactory-Immigration-Status-UIS-from-a-Managed-Ca.pdf | DHCS | 2026-09-01 | host copy (CenCal) | Version comparison only (grep, not a full read) | High |
| S03 | Fee-for-Service Transition FAQ for Providers: https://www.dhcs.ca.gov/wp-content/uploads/2026/08/Fee-for-Service-Transition-Provider-FAQ.pdf | DHCS | Sept 2026 | archive 2026-10-17 | Guide's Group B quote; services that continue; navigators | High |
| S04 | Medi-Cal FFS Provider Toolkit v1.0: https://www.dhcs.ca.gov/wp-content/uploads/2026/10/DHCS-FFS-Provider-Toolkit-68872c.pdf | DHCS | 2026-10-14 | archive 2026-10-17 | "Submit by" wording; accepting patients is a choice; TARs; transport enrollment | High |
| S05 | Fee-for-Service Transition member page: https://www.dhcs.ca.gov/medi-cal/updates/fee-for-service-transition/ | DHCS | undated | archive 2026-10-16 | Who is affected; duals; PACE | High |
| S06 | Immigration Status and Changes to Medi-Cal Eligibility (status table): https://www.dhcs.ca.gov/immigration-status-and-changes-to-medi-cal-eligibility/ | DHCS | undated | archive 2026-10-25 | Status-by-status table of who moves, age limits, dental, premiums | High |
| S07 | Medi-Cal Immigrant Eligibility FAQs: https://www.dhcs.ca.gov/medi-cal-immigrant-eligibility-faqs/ | DHCS | undated | archive 2026-10-17 | Freeze; premium ages. Stale on dental (still says July 1, 2026) | Medium |
| S08 | Medi-Cal Changes: https://www.dhcs.ca.gov/medi-cal/updates/medi-cal-changes/ | DHCS | undated | archive 2026-10-26 | Dated change list, including six-month checks on March 1, 2027 | High |
| S09 | Tracking Federal Impact: Medi-Cal Eligibility: https://www.dhcs.ca.gov/tracking-federal-impact-medi-cal-eligibility/ | DHCS | undated | archive 2026-08-24 | Work rules; six-month checks; retroactive coverage; litigation | High |
| S10 | 2026-27 Budget Act Highlights: https://www.dhcs.ca.gov/wp-content/uploads/2026/07/DHCS-FY-2026-27-Budget-Act-Highlights.pdf | DHCS | 2026-07-01 | archive 2026-08-10 | Savings; $39M; PPS and dental delays; MCO tax and targeted rates; 148,000 QNC | High |
| S11 | 2026-27 May Revision Highlights: https://www.dhcs.ca.gov/wp-content/uploads/2026/05/DHCS-FY-2026-27-May-Revise-Highlights.pdf | DHCS | May 2026 | archive 2026-10-22 | Rationale; $6B state-only managed care cost; QNC included in FFS shift | High |
| S12 | TBL fact sheet, Eliminate PPS for State-Only Services: https://www.dhcs.ca.gov/Budget/Documents/DHCS-TBL-Eliminate-PPS-for-State-Only-Services-Fact-Sheet.pdf | DHCS | 2025 (proposal) | archive 2026-04-07 | PPS and wrap mechanics; Medi-Cal Fee Schedule rate after elimination | High for mechanics; proposal text |
| S13 | Coverage Ambassadors bulletin: https://content.govdelivery.com/accounts/CAMEDI-CAL/bulletins/4269603 | DHCS | 2026-08-24 | direct | "Children and pregnant individuals" impacted; delays including Prop 56 | High |
| S14 | Medi-Cal Provider Enrollment FAQ: https://medi-calrx.dhcs.ca.gov/cms/medicalrx/static-assets/documents/faq/Medi-Cal_Provider_Enrollment_FAQ.pdf | DHCS / Medi-Cal Rx | 2026-04-03 | direct | 90 and 180 day response; effective date; ORP; MCP contract does not count; fee | High |
| S15 | Supplemental Claim Message: https://medi-calrx.dhcs.ca.gov/cms/medicalrx/static-assets/documents/provider/2026/02_A_Supplemental_Claim_Message_Provider_Enrollment.pdf | DHCS / Medi-Cal Rx | 2026-02-23 (stamped ARCHIVED) | direct | Superseded June 26, 2026 enforcement date; "90-180 days" | Medium, superseded on date |
| S16 | SMD #25-003: https://www.medicaid.gov/federal-policy-guidance/downloads/smd25003.pdf | CMS | 2025-09-30 | direct | Federal driver; what CMS actually allows; enforcement timing | High |
| S17 | CMS letter to Governor: https://www.dhcs.ca.gov/wp-content/uploads/2026/04/CA-Medicaid-Letter-Final.pdf | CMS | 2026-01-27 | archive 2026-09-18 | $1.6B recoupment; immigration enumerator request | High |
| S18 | The 2026-27 California Spending Plan: Health: https://lao.ca.gov/Publications/Report/5210 | LAO | 2026-10-19 | direct (read through WebFetch summary) | Enacted savings; premium range; dialysis; MCO tax; PPS delay | High for source; summarized read |
| S19 | The 2026-27 Budget: Medi-Cal at the May Revision: https://abgt.assembly.ca.gov/system/files/2026-05/initial-lao-analysis-of-medi-cal-at-may-revision.pdf | LAO | May 2026 | direct | Why all UIS services moved; open questions; caseload | High |
| S20 | Physician Rates in Medi-Cal: https://abgt.assembly.ca.gov/media/7649 | LAO | 2024-05-06 | direct | Managed care vs FFS rate evidence; 87.5% target; Prop 56 folded in | Medium, dated |
| S40 | W&I Code 14043.26: https://codes.findlaw.com/ca/welfare-and-institutions-code/wic-sect-14043-26/ | State statute via FindLaw | undated copy | direct (leginfo refused automated access) | 90 and 180 day limits; provisional status | Medium; confirm against leginfo |
| S41 | 45 CFR 164.506: https://www.law.cornell.edu/cfr/text/45/164.506 | Federal rule via Cornell LII | current copy | direct (eCFR redirected) | HIPAA use and disclosure with a former member | High |

## B. Primary: IEHP documents

| ID | Document and URL | Doc date | Route | Supports | Reliability |
|---|---|---|---|---|---|
| S21 | IEHP Fact Sheet: https://www.iehp.org/content/dam/iehp-org/en/documents/about/fact-sheet/IEHP_Fact_Sheet.pdf | Oct 2026 (PDF created 2026-10-01) | direct | Membership, provider network, market-share claim | High for its own counts |
| S22 | Governing Board Report #374: https://www.iehp.org/content/dam/iehp-org/en/documents/governing-board/governing-board-meetings/2026/august-2026/IEHP-Governing_Board_Reports_374-August_10_2026.pdf | 2026-08-10 | direct | **More than 100,000 / about 10%**; 370,000 work rules; finances; TNE | High; slide-level statement |
| S23 | Governing Board Report #373: https://www.iehp.org/content/dam/iehp-org/en/documents/governing-board/governing-board-meetings/2026/june-2026/IEHP-Governing_Board_Reports%20_373-June_8_2026_Meeting.pdf | 2026-06-08 | direct | About $21M CY2025 UIS risk corridor | High |
| S24 | Governing Board Report #372: https://www.iehp.org/content/dam/iehp-org/en/documents/governing-board/governing-board-meetings/2026/may-2026/IEHP_Governing-Board-Reports-372_May-11-2026.pdf | 2026-05-11 | direct | Community Reinvestment accrual | High |
| S25 | Governing Board Report #369: https://www.iehp.org/content/dam/iehp-org/en/documents/governing-board/governing-board-meetings/2026/february-2026/CY26_GB_IEHP-Governing-Board-Report-369_February_9_2026.pdf | 2026-02-09 | direct | Lapse rules; PCP capitation and P4P effect; risk corridor | High |
| S26 | Provider notice (UIS changes): https://www.providerservices.iehp.org/content/dam/provider-services-rd/en/documents/providers/plan-updates/provider_notices/2026/08---august/20260820%20-%20Unsatisfactory%20Immigration%20Status%20(UIS)%20-%20Medi-Cal%20Eligibility%20and%20Coverage%20Changes%20for%20Members.pdf | 2026-08-20 | direct | Says "adult" members only; "approval before January 1" | High as a record; scope superseded |
| S27 | Provider notice (coverage ending): https://www.providerservices.iehp.org/content/dam/provider-services-rd/en/documents/providers/plan-updates/provider_notices/2026/10---october/20261015%20-%20Unsatisfactory%20Immigration%20Status%20(UIS)%20IEHP%20Coverage%20Ending%20and%20Transition%20to%20Medi-Cal%20Fee-for-Service.pdf | 2026-10-15 | direct | "Apply and be approved"; 90-day prescriptions; CCS unaffected | High |
| S28 | Provider notice (survey): https://www.providerservices.iehp.org/content/dam/provider-services-rd/en/documents/providers/plan-updates/provider_notices/2026/10---october/20261028%20-%20IMPORTANT%20Unsatisfactory%20Immigration%20Status%20(UIS)%20Survey%20-%20Medi-Cal%20Fee-for-Service%20Participation.pdf | 2026-10-28 | direct | IEHP's provider participation survey | High |
| S29 | Provider notice (prescribers): https://www.providerservices.iehp.org/content/dam/provider-services-rd/en/documents/providers/plan-updates/provider_notices/2026/10---october/20261001%20-%20Medi-Cal%20Enrollment%20Required%20for%20Prescribers.pdf | 2026-10-01 | direct | Enforcement "soon", no date | High |
| S30 | Medi-Cal Eligibility and Benefit Changes: https://www.iehp.org/en/legal-and-privacy/medi-cal-policy-change | Updated 2026-08-13 | direct | IEHP's public change list | Medium; predates v2 and v3 |

## C. Secondary and research sources

| ID | Document and URL | Publisher | Doc date | Route | Supports | Reliability |
|---|---|---|---|---|---|---|
| S31 | Issue brief, Medi-Cal Enrollees with UIS: https://www.chcf.org/wp-content/uploads/2026/10/Medi-Cal-Enrollees-Unsatisfactory-Immigration-Status.pdf | CHCF / Aurrera Health Group | Oct 2026 | direct | 1.9M; 251,000 under 21; age table; county FFS provider counts; 58.7%; 16,000; 16%; $31M and $8M | High; relays DHCS deck not opened by us |
| S32 | Regional Market Report 2026: Inland Empire: https://www.chcf.org/wp-content/uploads/2026/09/Inland-Empire-Regional-Market-Data.pdf | CHCF | Cover April 2026; file 2026-09-17 | direct | 2,002,437; 94%; plan shares; workforce | High; 2024 data |
| S33 | Inland Empire RMR slides: https://www.chcf.org/wp-content/uploads/2026/06/InlandEmpireRMR2026_Slides.pdf | CHCF | 2026-06-15 | direct | Guide's "more than two million" and "94%" wording | High |
| S34 | Medicaid-to-Medicare Fee Index: https://www.kff.org/medicaid/state-indicator/medicaid-to-medicare-fee-index/ | KFF, from Urban Institute | May 2025 source | direct | US and CA fee index values | High for values; see rate caveat |
| S35 | Physicians urged to prepare: https://www.cmadocs.org/newsroom/news/view/physicians-urged-to-prepare-for-major-medi-cal-fee-for-service-transition-on-jan-1 | California Medical Association | 2026-10-13 | archive 2026-10-17 | **151,000 / 45,000 / 20,000** from DHCS webinar; county rank; 90 days; fee schedule | Medium-High; trade body reporting DHCS |
| S36 | UIS enrollees moving to FFS: https://www.cmadocs.org/newsroom/news/view/medi-cal-enrollees-with-unsatisfactory-immigration-status-moving-to-fee-for-service-in-2027 | CMA | 2026-09-11 | archive 2026-10-17 | Federal basis; FFS schedule replaces contract rates | Medium |
| S37 | QuickFacts, Riverside County: https://www.census.gov/quickfacts/riversidecountycalifornia | US Census Bureau | V2025 | archive 2026-10-18 | Guide's county snapshot | High |
| S38 | QuickFacts, San Bernardino County: https://www.census.gov/quickfacts/sanbernardinocountycalifornia | US Census Bureau | V2025 | archive 2026-10-22 | Guide's county snapshot | High |
| S39 | Study shows patients' insurance still determines physician access: https://www.commonwealthfund.org/publications/newsletter-article/study-shows-patients-insurance-still-determines-physician-access | Commonwealth Fund | 2012-08-06 | archive 2024-11-05 | Decker 2012 summary | Medium; old, secondary |
| S42 | CHC financial impact one-pager and full report: https://chapmanconsult.com/wp-content/uploads/2026/05/CHC-Financial-Impact-Policy-Changes_OnePager-05-18-2026.pdf ; https://chapmanconsult.com/wp-content/uploads/2026/05/HR1-Report-FINAL-May-2026.pdf | Chapman Consulting | May 2026 | direct | PPS revenue loss estimate; 2,118,287 UIS | Medium; assumptions stated, audience unknown |
| S43 | CEO Business Challenge: https://www.cpp.edu/cba/ceo-business-challenge/index.shtml | Cal Poly Pomona | 2026 | direct | Sponsor, dates, team size; no rubric or case file | High |
| S44 | UIS provider letter and FAQs: https://alamedaalliance.org/wp-content/uploads/PS_MCAL-PRVDR_UIS-Provider-Letter-FAQs_08172026-clean_faxed-08172026.pdf | Alameda Alliance | 2026-08-17 | direct | "Apply and be approved and enrolled" | Medium |
| S45 | UIS Transition alert: https://www.hpsj.com/unsatisfactory-immigration-status-uis-transition/ | Health Plan of San Joaquin | 2026-08-12 | direct (summary read) | Duals included; billing codes | Medium |
| S46 | UIS Transition Update: https://www.hpsj.com/uis-transition-update/ | Health Plan of San Joaquin | 2026-09-30 | direct (summary read) | Warm handoffs; CHW demand | Medium |
| S47 | 2027 Medi-Cal FFS Transition: https://thealliance.health/for-providers/resources/fee-for-service-transition/ | Central California Alliance | undated | direct (summary read) | FFS methodology may differ from contract rates; no payment after 12/31 | Medium |
| S48 | Preparing for the 2027 Transition: https://www.cencalhealth.org/providers/upcoming-medi-cal-changes/ | CenCal Health | undated | direct (summary read) | Locations of v1 to v3 of the guide | Medium |
| S49 | Medi-Cal changes coming Jan. 1, 2027: https://main.sbcounty.gov/2026/10/01/medi-cal-changes-coming-jan-1-2027-what-members-need-to-know/ | San Bernardino County | 2026-10-01 | direct (summary read) | County gives no local count | Medium |
| S50 | From Managed Care to Fee-for-Service: https://first5center.org/blog/from-managed-care-to-fee-for-service | First 5 Center | undated, 2026 | direct (summary read) | 38,000 children 0-5 (no source shown) | Low-Medium |

## D. Known but NOT read: excerpts from search results only

A human should open these. Any fact taken from them is labeled `[UNVERIFIED]` in the findings.

| ID | Document and URL | Publisher | Doc date | Why not read | What the excerpt suggests |
|---|---|---|---|---|---|
| U01 | SAC and BH-SAC deck, UIS to FFS: https://www.dhcs.ca.gov/wp-content/uploads/2026/09/09-22-26-SAC-BH-SAC-Meeting-Deck-UIS-to-FFS-Transition.pdf | DHCS | 2026-09-22 | Bot wall, no archive copy | "86% of rides ... through brokers who can't enroll"; "529,548 members" (population not identified); command center. Probably the richest single source |
| U02 | UIS to FFS Transition webinar: https://www.dhcs.ca.gov/wp-content/uploads/2026/09/UIS-to-FFS-Transition-Webinar-9-30-26_a8b203.pdf | DHCS | 2026-09-30 | Bot wall, no archive copy | Origin of the 151,000 / 45,000 / 20,000 figures |
| U03 | SAC and BH-SAC deck: https://www.dhcs.ca.gov/ru/file/10-28-2026-sac-bh-sac-meeting-deck-pdf/ | DHCS | 2026-10-28 | Bot wall, no archive copy | Newest DHCS update; content unknown |
| U04 | Draft Clinic Policy Letter 26-001: https://www.dhcs.ca.gov/ru/wp-content/uploads/2026/06/Draft-Clinic-Policy-Letter-PPS-State-Only-MC.pdf | DHCS | 2026-06-03 | Bot wall, no archive copy | Federally eligible pregnancy and emergency wrap continues; FFS guidance "forthcoming" |
| U05 | PN Addendum: https://www.dhcs.ca.gov/wp-content/uploads/2026/06/PN-Addendum-for-Clinic-Policy-Letter-PPS-State-Only-MC_9c393c.pdf and Addendum Three: https://www.dhcs.ca.gov/tl/wp-content/uploads/2026/07/Fqhc-PN-Addendum-Three.pdf | DHCS | 2026 | Bot wall, no archive copy | Revised timeline guidance forthcoming |
| U06 | FQHC PPS for State Only public notice: https://www.dhcs.ca.gov/Documents/FQHC-PPS-for-State-Only-Public-Notice.pdf | DHCS | 2026 | Bot wall, no archive copy | IHS/MOA, Tribal FQHCs and Urban Indian Organizations excluded from the change |
| U07 | APL 25-004: https://www.dhcs.ca.gov/formsandpubs/Documents/MMCDAPLsandPolicyLetters/APL%202025/APL25-004.pdf and Appendix A: https://www.dhcs.ca.gov/formsandpubs/Documents/MMCDAPLsandPolicyLetters/APL%202025/APPENDIX-A.pdf | DHCS | Feb 2025 | Bot wall; archive copy returned 403 | 5% of net income, 7.5% above a threshold; serves "communities in which the MCP operates" |
| U08 | Community Reinvestment FAQ: https://www.dhcs.ca.gov/calaim-transforming-medi-cal/community-reinvestment-cr-policy-and-frequently-asked-questions/ and page: https://www.dhcs.ca.gov/community-reinvestments/ | DHCS | 2026 | Archive copy contained only the wall | Cannot fund activities already in the MCP contract; must tie to community needs |
| U09 | Stakeholder News: https://www.dhcs.ca.gov/news/stakeholder-news-october-5-2026/ | DHCS | 2026-10-05 | Bot wall | $8M navigators through CPCA; 28 to 45 grantees |
| U10 | Prop 35 code list: https://www.dhcs.ca.gov/medi-cal-proposition-35-primary-and-specialty-code-list/ | DHCS | 2026 | Archive copy contained only the wall | Supplemental payments July to December 2026, pending SPA 26-0029 |
| U11 | Updated ORP bulletin: https://www.dhcs.ca.gov/vi/wp-content/uploads/2026/05/UpdatedMedicalRequirementsOrderingReferringPrescribingBulletin.pdf | DHCS | May 2026 | Bot wall | ORP-only enrollment does not pay for services furnished directly |
| U12 | Medi-Cal enrollment effective date page: https://mcweb.apps.prd.cammis.medi-cal.ca.gov/page/effective-date-of-enrollment ; bulletin: https://mcweb.apps.prd.cammis.medi-cal.ca.gov/news/33930.01 | DHCS | undated | Page needs JavaScript; no text returned | Effective date generally date complete package received |
| U13 | Transition stakeholder page and fact sheet: https://www.dhcs.ca.gov/providers-partners/medi-cal-fee-for-service-transition/ ; https://www.dhcs.ca.gov/wp-content/uploads/2026/08/Fee-for-Service-Transition-Fact-Sheet-General.pdf ; FAQ on the guide's own link: https://www.dhcs.ca.gov/hm/file/ffs-transition-provider-faq-pdf/ | DHCS | 2026 | Bot wall | Search excerpt says the change applies to all UIS members including babies and children. The guide's `/hm/` links could not be opened; S03 is the same document on its canonical path, not confirmed byte for byte |
| U14 | LHPC paper: "Medi-Cal FFS for UIS Population Jeopardizes Critical Health Care Services & Access" (no URL found) | Local Health Plans of California | accessed by CHCF 2026-07-31 | Not located | Known only through S31 |
| U15 | CHCF Medi-Cal Enrollment Tracking Tool: https://www.chcf.org/resource/medi-cal-enrollment-tracking-tool | CHCF | ongoing | Interactive tool; county views not confirmed | Possible county-level expansion totals. Not pursued, and needs an owner decision, because it may rest on the prohibited aid-category data |

## E. Searched, not found
| Item | Result |
|---|---|
| IEHP Case Document | Not found publicly. S43 links no case file |
| Financial Impacts Modeling Spreadsheet | Not found publicly |
| Competition rubric or judging criteria | Not found publicly. S43 states none |
| County-level UIS enrollee count for Riverside or San Bernardino | Not found. Only a rank order (S35) |
| Any DHCS rule for expedited PAVE processing tied to this transition | Not found |
| IEHP September or October 2026 board reports | Not found by search; not listed in results |
