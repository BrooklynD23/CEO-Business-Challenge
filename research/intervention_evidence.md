# Intervention evidence review (Phase 0)

Prepared 2026-11-02 for the IEHP CEO Business Challenge. Owner: intervention-evidence workstream.
Binding contract: `docs/phase0_contract.md`. No numeric MCDA scores are given here, by instruction.
Policy facts (who moves, what FFS covers, dates) belong to the policy workstream. Where an intervention's feasibility
depends on a policy fact, this file marks it **[POLICY-CONFIRM]**.

## Corrections added by the lead, 2026-11-02 (read first)

The research brief for this file wrongly told the author the moving group "appears to be adults". That was the lead's error, not the author's. `research/policy_verification.md` supersedes the following:

| Where | Text below says | Corrected |
|---|---|---|
| 0 scope warning 1; 5 "Adults vs children"; 6 assumption 9 | Moving group is adults; pediatric framing looks wrong | **Wrong.** No age exemption. Children not lawfully residing and adults 60+ move. Statewide about 251,000 of 1.9 million are under 21. Disregard assumption 9 |
| 5 state-policy overlay | Dental benefit ended July 2026 | Delayed to July 1, 2027; emergency-only for many UIS adults then. Inland Empire is on Dental FFS, so January 1 changes nothing for dental |
| 5 premium amounts | $30 vs $50 | $30 set, with May 2027 revision to set it between $30 and $50 |
| Item 7 | Unclear whether the fee index reflects FFS | KFF index is FFS-only. California 0.67 all services, 0.56 primary care. DHCS's 87.5% of Medicare target for primary care conflicts and is unresolved |
| Item 2, candidate C | Conversion of Group B is the most time-critical lever | Statewide, dormant FFS-enrolled providers (about 45,000) outnumber non-enrolled (about 20,000), so reactivation is likely the larger lever. Enrollment windows are 90/180 days with no expedited path found |
| Items 6, 8, 11 | ECM and Community Supports unresolved | ECM, CICM, Community Supports, CCM, TCS **end** on January 1. CHWs are not separately billable by non-tribal FQHCs/RHCs |
| 2.4, candidate B | FQHC payment unclear | PPS retained January 1 to June 30, 2027; fee schedule from July 1, 2027. An FQHC-anchored plan must address July |
| Item 9 | NEMT/NMT for FFS members unknown | Covered in FFS; transport providers must enroll. A DHCS deck reportedly says 86% of rides run through brokers who cannot enroll [UNVERIFIED]. If true, transport moves up in priority, and the Philadelphia null result is less relevant |

Remaining `[POLICY-CONFIRM]` tags: check against the policy file before citing.

## 0. How to read this file

**Evidence labels** (contract): `[VERIFIED: source id, 2026-11-02]` means I retrieved the source and read the relevant text. `[ESTIMATE: ...]` is my arithmetic or judgement. `[UNVERIFIED: ...]` means the claim comes only from a web-search result summary, a blocked page, or a source I could not open. The search tool returns AI-written summaries, so every claim that rests only on one is marked `[UNVERIFIED]`, even when it looks plausible.

**Read status** (also in the Sources section): `R-local` = PDF text extracted and read by me. `R-fetch` = page retrieved through the WebFetch tool, which returns a model-written extract of the page, not raw text. `SNIP` = search-result summary only, source not opened. `BLOCKED` = fetch returned nothing usable (several DHCS pages sit behind bot protection; I did not try to bypass it).

**Primary or secondary**: primary = the study, dataset or agency document itself. Secondary = news, press release, advocacy summary, or another author's summary.

**Scope warnings**
1. The moving population is defined by immigration status and appears to be adults. Most of the best evidence below is from general Medicaid populations, and much of it is from adults in other states. Transfer to UIS adults in the Inland Empire is a judgement, not a finding.
2. Nothing here is a sub-county estimate of immigration status. Anything I say about geography uses supply data or all-Medi-Cal totals only (contract rule 2).
3. Window: 2026-11-02 to 2026-12-31 is 59 calendar days, roughly 40 business days once holidays are removed [ESTIMATE].

---

## 1. Bottom line first

1. **Nothing found studies the direction of this transition (managed care to FFS) for Medicaid adults.** The closest evidence is the reverse direction (FFS to managed care in North Carolina), plan-to-plan transitions, and the Medi-Cal Rx pharmacy move. That is the most important evidence gap in this file.
2. **Listed is not available.** Audit and secret-shopper evidence gives a defensible planning range of roughly 40 to 65% of listed Medicaid providers actually able to offer a new-patient appointment, and care is concentrated: about 25% of primary care physicians in managed-care networks provided 86% of Medicaid primary care in four states. For FFS-enrolled lists specifically, no direct evidence found.
3. **The binding constraint in the 60-day window is provider and clinic capacity plus administrative speed, not information.** Interventions that need new capital, new hiring, rate changes, or new payment pathways mostly cannot land by 1/1/2027. Interventions that move existing capacity (enrollment help for the right providers, FQHC partnerships, continuity handoffs for high-risk members, scheduling and warm referral) can.
4. **Chilling effects are measurable and current.** Any intervention that is visible, outdoor, or proactively contacts UIS members carries documented attendance and enrollment risk (section 5).
5. **Several listed ideas are not interventions.** Geographic gap mapping and the digital twin are planning tools (category A). AI matching redistributes demand among existing supply and cannot create appointments.

---

## 2. The five research questions

### 2.1 How do Medicaid patients fare when moved between managed care and FFS?

**Direct evidence for managed care to FFS in adults: no direct evidence found.** I searched for natural experiments on carve-outs and reverse transitions. Findings that are adjacent:

| Study / event | Design | What happened | Relevance and limits | Source |
|---|---|---|---|---|
| North Carolina, July 2021, 1.6 million beneficiaries moved FFS to managed care | Observational, one health system: survey of 398 Medicaid enrollees plus EHR data on 4,859 Medicaid vs 5,137 privately insured patients | Primary care visits fell 7.1% among Medicaid enrollees relative to privately insured. 77.3% reported the plan was auto-assigned. 79% got no social-needs help. 5.9% were assigned a different PCP | Opposite direction, one system, coincided with COVID, so the 7.1% is not causal. It shows the size of a "soft" disruption when members are not guided [VERIFIED: S24, 2026-11-02] | S24 secondary R-fetch |
| Medi-Cal Rx, 1/1/2022, about 14 million members moved from plan-run pharmacy benefit to a state-run FFS contractor | Journalism, no evaluation | More than 95,000 prior-authorization requests in weeks. Call waits up to 8 hours. 100 of 220 call-center staff absent in the first two weeks. Plans did not send all needed data. A promised 180-day grandfathering was not always honored. Some members went days or weeks without drugs. DHCS called it "unacceptable" and allowed 2-week emergency fills [VERIFIED: S23, 2026-11-02] | The closest California analog for a state-run FFS handoff. The failure points were data transfer, authorization carry-over and call capacity, not network size. No independent evaluation of denial rates found | S23 secondary R-fetch |
| Minnesota 2016 competitive bidding forced more than half of enrollees to change plans | University dissertation, claims | Reported 30% reductions in use across a wide range of services, concentrated in one plan; more new-provider visits [UNVERIFIED: S44, search summary of an unpublished dissertation] | Low confidence | S44 SNIP |
| Illinois managed care rollout, seniors and disabled | Cross-sectional survey and DiD abstracts | 66% of survey respondents in early pilot regions had to see at least one new doctor vs 40% in later regions; managed care enrollment itself was not related to unmet need, but less continuity decreased health services appraisal [UNVERIFIED: S45, search summary] | Shows continuity loss, not magnitude for this case | S45 SNIP |
| California seniors and persons with disabilities (SPD) mandatory managed care, 2011-12 | Health Affairs title only: "Medicaid Beneficiaries In California Reported Less Positive Experiences When Assigned To A Managed Care Plan" | [UNVERIFIED: S46, title seen in a search result; abstract not read] | Opposite direction | S46 SNIP |

**FFS vs managed care access, head to head.** No national or recent comparison of new-patient acceptance by payment model found. One California physician survey (Backus 2001) reportedly found that among physicians taking new Medi-Cal patients, 62% of specialists and 80% of PCPs would take Medi-Cal managed care patients, implying specialists were more willing to take FFS [UNVERIFIED: S40, search summary; 25 years old].

**What this implies for the model:** use plan-switch and continuity-loss evidence as a lower bound on disruption, and treat Medi-Cal Rx as the best California operational analog. The Medi-Cal Rx lesson is that the stated continuity rule and the operational reality diverged in the first 2 to 6 weeks.

### 2.2 Enrolled vs actually available providers (ghost networks)

| Source | Design and scope | Result | Label |
|---|---|---|---|
| HHS OIG OEI-02-13-00670 (Dec 2014) | Secret-shopper calls to a stratified random sample of 1,800 primary care providers and specialists listed by about 200 Medicaid managed care plans in 32 states | Slightly more than half could not offer appointments to enrollees. 35% could not be found at the listed location. 8% were there but not in the plan. 8% not accepting new patients. Among those offering appointments, median wait 2 weeks, over 25% waited more than 1 month, 10% more than 2 months. PCPs were less likely to offer appointments than specialists | [VERIFIED: S2, 2026-11-02] primary. S3 corroborates (secondary) |
| Ludomirsky et al., Health Affairs 2022;41(5):760-768 | Managed-care network directories in 4 states, 2015-17 data | About one-third of outpatient PCPs and specialists in the sample saw fewer than 10 Medicaid beneficiaries per year. 25% of PCPs gave 86% of primary care; on average 25% of specialists gave 75% of specialty care. Authors say network adequacy standards may not reflect real access | [VERIFIED: S1 abstract, 2026-11-02] primary |
| Candon et al., JAMA Intern Med 2018 research letter | Simulated-patient audit of in-network primary care practices in 10 states, 2012-13 vs 2016 | New-patient appointment availability for Medicaid callers 57.9% to 63.2% (+5.4 pp, 95% CI 2.1 to 8.6); private 84.7% to 83.2% (not significant). Short waits (1 week or less) for Medicaid fell 6.7 pp | [VERIFIED: S5, 2026-11-02] primary. Only practices already in-network |
| HHS OIG report on maternal-health listings (reported June 2026) | Directories of Centene, Elevance, UnitedHealthcare Medicaid plans in 5 states | 9% of listed providers out of network overall (Centene 22%, Elevance 4%, UHC 6%). In-network providers missing from directories 35% / 11% / 25%. Inaccurate contact information 37% / 41% / 22%. A federal secret-shopper requirement starts 7/10/2028 | [VERIFIED: S4 secondary news report, 2026-11-02]. The OIG report itself was not opened |
| California physician survey (UCSF for CHCF, 2015, about 6,000 respondents) | Voluntary survey with license renewal | 64% of California physicians had any Medi-Cal patients in 2015, down from 69% in 2013. 40% of doctors provided 80% of Medi-Cal visits. Only about 37% of psychiatrists accepted Medi-Cal | [VERIFIED: S26, 2026-11-02] secondary. Self-report; response rate not stated. A "60% accept new patients" figure appeared in a search summary only [UNVERIFIED: S26b] |
| California State Auditor 2023-115 and 2014-134 | Audits of DHCS oversight | 2023-115: 43% of urgent psychiatry appointments DHCS surveyed in 2022 exceeded the 96-hour standard. 2014-134: DHCS did not verify the provider-network data plans submit [UNVERIFIED: S33, search summary] | |
| Denti-Cal (California FFS dental) | Reporting on participation | Estimates of dentist participation range from about 25% to 66% depending on definition. 23% of eligible adults with FFS Denti-Cal saw a dentist in July 2017 to June 2018 [UNVERIFIED: S43, search summary] | An in-state example that FFS enrollment is not access |

**Empirically grounded range [ESTIMATE: judgement across S2, S5, S26]:** about 49% (OIG 2014, offered an appointment), 60 to 64% (California physicians self-reporting any or new Medi-Cal acceptance, 2015), and 63% (Candon 2016, in-network practices only) bracket the share of listed providers who can take a new Medicaid patient. A planning range of **40 to 65%** is defensible, with a low case around 30% for specialty and behavioral health. **The effective capacity is more concentrated than the headcount:** a model should weight by volume, not count enrolled providers equally.

**What is missing:** no audit of FFS-enrolled (as opposed to managed-care-listed) Medi-Cal providers, none specific to Riverside and San Bernardino, and nothing on whether providers who accept managed-care Medi-Cal will take FFS-only UIS patients. A DHCS-enrolled provider list will not show new-patient acceptance (student guide, Source E notes).

### 2.3 FQHC and safety-net reliance, immigrant access, chilling effects

**FQHC scale.**
- California health centers, 2025 reporting year: 170 awardees, 5,900,539 patients, 71.79% Medicaid/CHIP, 9.31% uninsured, 64.02% Hispanic or Latino, 39.02% limited English proficiency [VERIFIED: S18, 2026-11-02] primary.
- National 2025: 32.7 million patients, 48% Medicaid, 17% uninsured, 144 million visits (about 4.4 per patient, my division), 13% of visits by telehealth [VERIFIED: S17, 2026-11-02] secondary (KFF analysis of HRSA UDS).
- Inland Empire: county-run Riverside University Health System network of 13 FQHCs served over 95,000 patients in 2023 (about 50% more than 2019); more than 50 other CHCs are core outpatient providers; "a growing share of the region's population relies on CHCs" [VERIFIED: S15 slides, 2026-11-02] primary-analysis slides.
- Share of **Medi-Cal** or **UIS** care delivered by FQHCs in the Inland Empire: **no direct evidence found**.

**Immigrant reliance on safety-net clinics.** KFF/NYT 2025 survey: 46% of likely undocumented immigrant adults uninsured vs 6% of US-born citizens [VERIFIED: S16, 2026-11-02]. A search summary attributes to PPIC that 73% of undocumented immigrants with a usual source of care name a clinic, and to a UCLA-linked CHIS analysis (2011-2018) that 60% of undocumented immigrants had a usual source of care vs 75.7% of documented immigrants and 85.9% of citizens [UNVERIFIED: S42; PPIC page returned 403, figures not confirmed]. Pre-expansion California research also points to community clinics as the main safety-net source (Health Affairs 2013, title only seen) [UNVERIFIED].

**Randomized evidence on reducing friction in this population:** ActionHealthNYC (2016-17) randomly arranged initial primary care appointments for 2,428 undocumented immigrants. Abstract: self-reported access up and ED visits down 23% (NBER version 21%), concentrated in high-risk people (32% in the AER abstract, 42% in the NBER version) [VERIFIED: S30 abstract via IDEAS, 2026-11-02; the two versions disagree and I did not reconcile them]. This is the single best study found for a UIS adult population, and the intervention was **scheduling and warm referral**, not new capacity.

**Chilling-effect evidence (current).**
- KFF/NYT survey of immigrants, Aug to Oct 2025: 41% of immigrant adults worry they or a family member could be detained or deported (26% in 2023); 29% skipped or postponed health care (22% in 2023); about half (51%), and 78% of likely undocumented adults, worry providers might share immigration information with enforcement [VERIFIED: S16, 2026-11-02].
- UCLA LPPI (July 3, 2026), DHCS monthly data: adult expansion enrollment fell by about 71,000 from June to December 2025 (1.45 million to 1.38 million). The July-Dec decline was 4.8% for expansion vs 2.3% for non-expansion adults. Authors decompose about 70,000: 48% in line with broader Medi-Cal trends, 20% (about 13,700) attributable to ICE arrests directly (upper bound), 33% (about 22,900) unexplained and "consistent with a chilling effect". They state the analysis is descriptive, not causal, and that the May 2025 freeze proposal may also have contributed [VERIFIED: S20, 2026-11-02] primary.
- Mobile clinic visits: UCSF-Fresno reports about 36% decline (average 34 patients per outing in 2024, about 22 recently); Saint Agnes rural van 15 to 20% [VERIFIED: S21 news report, 2026-11-02] secondary, physician-reported, not a study.
- Over 86,000 immigrants without legal status left or were denied Medi-Cal in Jan and Feb 2026 (Public Health Watch analysis); enrollment peaked at 1.48 million in May 2025 [VERIFIED: S22 secondary, 2026-11-02]. These sources attribute this to the freeze, ICE data sharing, and federal law together.
- Public charge, 2019: 18% of adults in California immigrant families said they or a family member avoided public benefits (12% in 2018) [UNVERIFIED: S39, search summary of Urban/CHCF].

**Implication.** Demand from UIS adults is endogenous to how the transition is communicated and who is seen contacting them. Any model that treats "moving members" as a fixed pool of demand will overstate utilization. Equally, outreach that is not trusted will under-reach.

### 2.4 FQHC capacity and panel size

- **Panel-size literature.** Altschuler et al., Ann Fam Med 2012;10(5):396-400 (modelling, not an empirical trial): with team-based task delegation a primary care team could reasonably care for 1,947, 1,523 or 1,387 patients under three delegation scenarios; they cite an average US panel of about 2,300 and note a 2,500 panel would need about 21.7 physician hours a day [UNVERIFIED: S31, search summary; I did not open the paper]. I found no NCQA figure and no Medicaid- or FQHC-specific defensible panel number. **A panel-size cap for FFS physicians in this model should be treated as an input range, not a finding.**
- **FQHC staffing ratio from UDS (order of magnitude).** California 2022: 3,474 physician FTEs and 2,396 NP/PA/CNM FTEs; 5,312,677 total patients (all services) [VERIFIED: S19, 2026-11-02] secondary (NACHC fact sheet of UDS). Dividing gives about 900 patients per physician-or-NP/PA FTE [ESTIMATE: 5.31 million / 5,870]. Mixed years if combined with 2025 patients (5.16 million medical patients [VERIFIED: S18]), which gives about 880 [ESTIMATE]. UDS counts any patient with a visit, so this is not a panel size and cannot be read as headroom. **FQHC absorbable capacity: no direct evidence found.**
- **Group visits** (the candidate named). Housden et al., CMAJ 2013 meta-analysis: 13 RCTs, 2,319 people, HbA1c lower by about 0.46 percentage points; no clear effect on quality of life; no data on clinician capacity or access [UNVERIFIED: S32, search summary]. A commentary claim that group visits raise access is not trial evidence. **As a capacity multiplier for new patients: no direct evidence found.**
- **Extended hours:** no direct evidence found for a Medicaid FQHC effect on new-patient absorption.
- **Constraint that matters more:** FQHC finance. The Inland Empire CHC leaders and CHCF flagged Medi-Cal cuts as a threat to site and service expansion [VERIFIED: S15, slide 19-20]. A search summary says DHCS postponed the move of state-only (UIS) FQHC services off the prospective payment system from 7/1/2026 to 7/1/2027, and a news report says clinics expect large losses when it happens [UNVERIFIED: S35; DHCS notice returned empty; CPCA page confirms only that a report estimates the impact of "proposed elimination" of PPS for state-only populations] **[POLICY-CONFIRM: FQHC payment for UIS services after 1/1/2027.]** If clinics are paid less for UIS patients, their incentive to absorb them falls.

### 2.5 Lessons from earlier transitions

| Event | What is known | What is not |
|---|---|---|
| 2024 Medi-Cal managed care plan transition (about 1.2 million members changed plans; Health Net to Molina in LA, Kaiser expansion) | DHCS design: continuity of care up to 12 months with a provider who agrees to payment terms; enhanced protections for people with identified vulnerabilities; grievance rate 0.123% vs 0.145% baseline in one DHCS slide [UNVERIFIED: S41, search summary of DHCS slides; DHCS pages BLOCKED] | Member-level outcomes. A NORC evaluation of access, quality and continuity is under way; the CalAIM 1115 interim evaluation could not be fetched (empty). **No outcome data found.** |
| Medi-Cal Rx (2022) | See 2.1 | Independent denial-rate or health-outcome evaluation: none found |
| Unwinding (2023-25) | About 11 million renewals, about 2 million disenrolled, about two-thirds procedural; people with chronic conditions, disabilities or limited English proficiency faced more barriers; reinstatement was about 15% of initial disenrollees (268,533 of 1,771,109; the 15.2% is my division) [VERIFIED for the two-thirds and the groups: S29, 2026-11-02; reinstatement counts UNVERIFIED: search summary] | Health outcomes of the gap. These were coverage losses, not network losses, so only analogous |
| Texas, Illinois, other states | Mostly policy documents | |

**Lesson for planning:** the places a state-run handoff fails are (a) data transfer from plans, (b) carry-over of authorizations and care plans, (c) call-center and phone capacity, and (d) communications to members who do not read mailed notices. Each maps to an intervention below (continuity handoffs, navigation, language-concordant outreach).

---

## 3. Summary matrix (no scores)

Time to deploy: **L** = lands by 1/1/2027 if started now; **P** = partial pilot by 1/1; **N** = realistically after 1/1/2027. These are judgements [ESTIMATE].

| # | Intervention | Cat. | Strongest relevant evidence | Cost evidence | Time | Authority | Policy facts to confirm |
|---|---|---|---|---|---|---|---|
| 1 | Geographic gap mapping | A | Methods literature only (2SFCA); no validation against outcomes | Staff time only; no cost source needed | L | IEHP | Sub-county UIS demand is barred by contract; supply and all-Medi-Cal only |
| 2 | Provider FFS enrollment conversion | C (enables B) | No direct evidence found for conversion programs; admin-burden literature | PAVE application is free in principle; support cost no direct evidence found | P | Provider applies, DHCS approves, IEHP persuades | PAVE current processing time; fast-track; which Group B providers matter |
| 3 | AI patient-provider matching | C | None for Medicaid. Vendor claims only | No direct evidence found | N (P as rules-based) | IEHP | Whether IEHP may hold FFS-provider data and contact FFS members |
| 4 | Mobile clinics | B | Descriptive and modelled ROI only; strong chilling exposure | Surveyed programs about $479k to $822k per year; $150 to $243 per visit | N | IEHP or partner, county | Whether FFS reimburses mobile units for UIS |
| 5 | Telehealth expansion | B | Use is lower among Medi-Cal and limited-English users; phone visits rated similar | No direct evidence found for platform cost | L (existing) / N (new) | Provider, IEHP | FFS telehealth and interpreter billing |
| 6 | Vulnerable-patient protection and care navigation | C (B for handoffs) | CHW RCT (secondary outcomes); ActionHealthNYC; Medi-Cal Rx lessons | $1,721 per patient (IMPaCT, 2018 dollars) | P | IEHP until 12/31, DHCS after | Which IEHP benefits (ECM, Community Supports) end for FFS members |
| 7 | Financial and administrative provider incentives | C | National audit evidence on fees and billing friction; modest effects | Fee gap quantified; incentive cost no direct evidence found | P (admin) / N (rates) | DHCS, legislature; IEHP only within its own contracts | Whether IEHP may pay non-contracted FFS providers |
| 8 | Community healthcare partnerships | C/B | ActionHealthNYC type linkage; trust literature | No direct evidence found | P | IEHP, CBOs, FQHCs | Data-sharing limits |
| 9 | Transportation assistance | C | Rideshare RCT null (Medicaid, Philadelphia) | About $42 per ride-day (FFS NEMT national, mixed modes) [ESTIMATE] | P | DHCS (FFS NEMT/NMT), IEHP | Whether FFS UIS members have NMT/NEMT and need certification |
| 10 | Transition digital twin | A | No direct evidence found | No direct evidence found | P (simple model) | IEHP | Needs data on movers not public |
| 11 | Community health workers / promotores | C | RCTs in low-income and Latino populations; mixed | $1,721 per patient; $567,951 per 6-CHW team | P | IEHP, CBOs, DHCS (benefit) | Whether Medi-Cal CHW benefit is billable for UIS in FFS |
| 12 | FQHC capacity as primary absorber | B | Reliance data strong; absorptive capacity no direct evidence found | Not estimable | P | FQHCs, DHCS | PPS treatment of UIS services |
| 13 | Provider-enrollment concierge | C | None direct | No direct evidence found | L | IEHP | Same as 2 |
| 14 | Complex-care continuity handoffs | C/B | Operational lessons; no Medicaid plan-change trial | Care manager cost no direct evidence found | L (list-based) | IEHP now, DHCS later | Record-transfer and consent rules |
| 15 | Language-concordant scheduling | C | Systematic review mostly observational | No direct evidence found | L | IEHP, providers | FFS interpreter reimbursement |
| 16 | Pharmacy-based care | B | Pharmacy benefit already FFS since 2022; outcomes evidence not found | Pharmacist rate stated as 85% of physician rate (2019 advocacy blog) | N/P | Pharmacies, DHCS | Whether AB 1114 pharmacist services are billable to FFS |
| 17 | eConsult for specialty | B/C | Pre-post studies in safety-net systems | None reported | N/P | Provider organizations | FFS payment for eConsult codes |
| 18 | Specialty referral pathways | B/C | Same as 17 and ActionHealthNYC | No direct evidence found | P | IEHP, providers | |

---

## 4. Evidence by intervention

Format: **Mechanism / Population / Evidence / Cost / Time / Authority / Risks / Measurement / Preliminary view**. Cost figures are in nominal dollars of the study year.

### 1. Geographic gap mapping (A)
- **Mechanism:** shows where supply is thin so other resources can be placed. Does not itself improve access.
- **Population:** all Medi-Cal in two counties; no UIS-specific sub-county layer (contract rule 2).
- **Evidence:** the common spatial method (two-step floating catchment area) is sensitive to catchment size, population inputs and travel mode, and the sources I saw found no validation against utilization or outcomes [UNVERIFIED: S47, search summary]. HPSA scores are for all providers (student guide). Enrolled-provider counts overstate availability by a factor documented in 2.2.
- **Cost:** analyst time. No direct evidence needed.
- **Time:** can finish before 1/1.
- **Authority:** IEHP.
- **Risks:** a ZIP-level ratio gives false precision; ranking by raw provider counts ignores concentration (25% of providers give most care). Publishing a UIS-demand map would be harmful and is barred.
- **Measurement:** compare map-predicted gap areas to a verified-availability call sample; report agreement.
- **View:** necessary for allocating anything else; not an intervention. Use a volume-weighted, availability-adjusted supply measure.

### 2. Provider FFS enrollment conversion (C, enabling)
- **Mechanism:** converts Group B providers (IEHP-network only) into Group A (both), so moved members keep their doctor. The state says providers not enrolled in FFS cannot care for UIS members after 12/31/2026 (student guide, quoting DHCS FAQ).
- **Population:** high-volume IEHP providers who currently see members expected to move. Provider-level lists must not leave the analysis (contract rule 4).
- **Evidence:** no direct evidence found on the effect of enrollment-assistance programs. Related: physicians report administrative burden and payment friction as reasons to limit Medicaid (S26); incomplete or denied Medicaid claims cost 17.4% of claim value vs 4.9% Medicare and 2.8% commercial, over 25% in California, and a 10-point rise in incomplete payments cut Medicaid acceptance by about 1 point [VERIFIED: S25 digest of NBER WP 29010, 2026-11-02]. This suggests enrolling is necessary but not sufficient: a provider who enrolls and then faces FFS billing friction may not take new FFS patients.
- **Time constraint:** DHCS has a statutory ceiling of 180 days to act on an application; older figures give averages of 45 to 59 days, with paper applications at 90 to 180 days, and "complete and correct" applications are faster [UNVERIFIED: S34, search summary, no 2025-26 figures found]. **[POLICY-CONFIRM: current PAVE turnaround, any fast-track or provisional enrollment, and whether an application filed by a given date can be effective 1/1/2027.]** If the average is 45 days or more, applications filed after about mid-November risk missing 1/1 [ESTIMATE].
- **Cost:** no direct evidence found. A concierge team is staff time.
- **Authority:** the provider applies; DHCS approves; IEHP can only inform, help, and (if allowed) incentivize.
- **Risks:** enrolls providers who then do not accept FFS patients ("enrolled" does not mean "accepting", student guide); effort spent on low-volume providers.
- **Measurement:** applications started, complete on first submission, approved by 12/31; then share of enrolled providers who bill any FFS claim for a transitioning patient in January-March 2027.
- **View:** the most time-critical lever, and the one with the least evidence. Target by volume, not by headcount.

### 3. AI-assisted patient-provider matching (C)
- **Mechanism:** assigns members to providers by language, location, specialty, and acceptance of new patients.
- **Evidence:** no direct evidence found for Medicaid. Vendor materials cite randomized or algorithm-comparison results, none peer-reviewed for Medicaid (Lyra mental-health algorithm comparison; Stellation claim of a 10% cost saving; UnitedHealthcare search tool with no evaluation found) [UNVERIFIED: S48, search summaries]. Its value depends on a **fresh, verified availability list**. Directory inaccuracy (S4: 22 to 41% inaccurate contact data in some plans) and the 49 to 65% availability range (2.2) mean the data layer, not the algorithm, is the bottleneck.
- **Closest evidence for the mechanism:** ActionHealthNYC (human-arranged first appointments for undocumented adults) reduced ED use about 21 to 23% (S30). That suggests matching and booking support can matter; it does not show that AI does it better than staff.
- **Cost:** no direct evidence found.
- **Time:** a rules-based matching script and a call-verified list are feasible by 1/1; a trained model is not.
- **Authority:** IEHP; data-sharing with DHCS about FFS members is **[POLICY-CONFIRM]**.
- **Risks:** presents unverified supply as real; algorithm bias on language or geography; pushing demand onto the few providers who accept Medicaid (concentration).
- **Measurement:** booked-and-attended rate within 30 days of matching vs unmatched comparison; accuracy of match against a call sample.
- **View:** treat as a scheduling-and-verification workflow; "AI" adds little without verified supply.

### 4. Mobile clinics (B)
- **Mechanism:** brings primary care to where people are; useful where there is no clinic nearby or trust in fixed sites is low.
- **Evidence:** (a) Family Van, Boston, ROI model reports $36 per $1 invested; annual cost $565,700 (the abstract says $567,700), 4,848 visits; the model assumes about 80% of visits would otherwise have been preventable ED visits, uses 2005 costs and a 1990 life-year value, and the extraction flagged internal arithmetic inconsistencies [VERIFIED: S9, 2026-11-02; arithmetic inconsistencies per the tool extract, not independently checked]. I regard the 36:1 as unsupported for planning. (b) Literature review of mobile clinics: findings I could not open [UNVERIFIED: S11]. (c) Survey of 96 programs in four southeastern states, 17 responded, 15 analysed (convenience sample): mean annual operating cost (2018 dollars) $479,092 preventive, $821,586 primary care plus preventive, $2.26 million dental; average cost per visit $243 preventive, $150 primary care/preventive, $123 dental; average visits per year 2,782 preventive, 3,956 primary care/preventive; labor 65 to over 90% of cost; capital reported only as depreciation share (5% for preventive and primary care) [VERIFIED: S10, 2026-11-02]. **Capital purchase cost: no direct evidence found in sources read.**
- **Per-visit cost check:** Family Van $565,700 / 4,848 visits is about $117 per visit [ESTIMATE: arithmetic].
- **Capacity:** about 3,000 to 4,000 visits per van-year in the surveyed programs; scale to need before considering [ESTIMATE].
- **Time:** purchase or lease, licensing, staffing, and site agreements: not a 60-day project. Existing county, FQHC or university vans could add stops sooner (UCSF-Fresno and Saint Agnes models in S21).
- **Authority:** IEHP funds; a licensed clinic or county operates; DHCS payment rules apply.
- **Risks:** documented visit declines of 15 to 36% in 2025 (S21); episodic care does not replace continuity; billing under FFS unknown **[POLICY-CONFIRM]**.
- **Measurement:** unique patients, return visits within 90 days, linkage to a continuity site, ED use for linked patients.
- **View:** a niche access tool; probably later than 1/1 and not the main absorber.

### 5. Telehealth expansion (B)
- **Mechanism:** adds appointments without travel or clinic space; phone and video.
- **Evidence:** 2021 CHIS: 49% of California adults used telehealth; use tracks overall doctor visits; uninsured 18%; people on Medi-Cal used less than people with employer or private coverage; among non-English speakers, those speaking English "not well" were less likely (38.3% vs 43.5%) [VERIFIED: S28, 2026-11-02, partial read]. Video visits were rated worse by limited-English users, phone visits similar (JAMA Netw Open analysis of CHIS 2021) [UNVERIFIED: S49]. Medi-Cal made payment parity for telehealth permanent in 2022 (S28 text). California FQHCs: 99% use telehealth (NACHC 2022 fact sheet, S19); national share 13% of visits (S17).
- **Cost:** no direct evidence found for platform or per-visit implementation cost in sources read.
- **Time:** existing provider telehealth can be promoted now; new platforms or interpreter-integrated video will not be ready.
- **Authority:** providers, IEHP; FFS billing rules **[POLICY-CONFIRM]**.
- **Risks:** digital divide and LEP; privacy concerns among immigrants (no direct evidence found); does not fix specialty, lab or imaging needs.
- **Measurement:** share of visits by modality and language; completion; downstream ED use.
- **View:** most useful as audio-first, language-supported follow-up for continuity cases; not a capacity solution for first visits.

### 6. Vulnerable-patient protection and care navigation (C, with B elements)
- **Mechanism:** identify high-risk members (pregnancy, insulin, dialysis, cancer, serious mental illness, recent hospitalization) before 1/1; transfer care plans; make sure each has an enrolled FFS provider and medication supply; follow up by phone.
- **Population:** high-risk subset of moving adults. Defining the subset using diagnosis and utilization (not immigration status) is IEHP's call and **[POLICY-CONFIRM]** for what data may be used.
- **Evidence:** ActionHealthNYC: effect concentrated among high-risk participants (S30). IMPaCT CHW RCT (592 patients, mean age 52.6, 94% African American, three Philadelphia sites): primary outcome (self-rated physical health) null (DiD -0.7, 95% CI -2.2 to 0.7, p=0.30); secondary results: hospital days 155 vs 345 at 6 months, 30-day readmission OR 0.3 (95% CI 0.1 to 0.9) [VERIFIED: S8, 2026-11-02]. Medi-Cal Rx lessons (2.1) show the failure points are carry-over and data, not network.
- **Cost:** IMPaCT team of 6 CHWs: $567,950.82 per year in one fiscal year (6 CHWs $307,550; supervision and support $146,667; equipment and overhead), $1,721.06 per patient; each CHW 55 patients per year, team caseload 330 [VERIFIED: S7, 2026-11-02, Philadelphia, 2018-era dollars]. A care manager for list-based handoffs: no direct evidence found.
- **Time:** a risk-stratified list and phone outreach is feasible by 1/1; CHW hiring and training is not.
- **Authority:** IEHP controls this until members leave its plan. After 1/1 the state and FFS providers are responsible. **[POLICY-CONFIRM: whether ECM and Community Supports end for moved members.]**
- **Risks:** list-based outreach to a UIS-defined group is a data-sharing and trust hazard; use medical need, not status, and do it through trusted contacts; incorrect lists.
- **Measurement:** share of listed members with a named enrolled FFS provider and a visit within 60 days of 1/1; missed medication refills; ED and inpatient use vs. a comparison group.
- **View:** the strongest candidate for the window, because it uses existing authority and staff. Note its evidence is inference from adjacent studies.

### 7. Financial and administrative provider incentives (C)
- **Mechanism:** pay or simplify so more providers enroll and take FFS patients.
- **Evidence:**
  - California FFS fees: Medicaid-to-Medicare fee index 2024 for California 0.67 (all services) and 0.56 (primary care) vs US 0.75 and 0.66; in 2019 California primary care was 0.76 [VERIFIED: S27, 2026-11-02]. Whether this fee index reflects FFS or managed care rates is not stated on the page [UNVERIFIED].
  - Candon et al. found Medicaid appointment availability rose 5.4 pp between 2012-13 and 2016 in 10 states (S5). A search summary reports a "$10 fee change = 1.7 pp availability" estimate and a 2015 NEJM fee-bump audit; I did not confirm either [UNVERIFIED: S6].
  - Billing friction reduces participation (S25). California physicians cite low pay and administration (S26).
  - MACPAC (2025) says earlier work linked rates to acceptance but later analyses did not find the correlation [UNVERIFIED: S40].
  - One-time enrollment bonuses: no direct evidence found.
- **Cost:** fee gap can be computed from rate tables; bonus cost no direct evidence found.
- **Time:** FFS rate changes are DHCS or legislative and are not a window option. Plan-funded incentives, prompt-payment help, and claims support can be started now if legally allowed.
- **Authority:** DHCS and legislature for rates; IEHP only through its own contracts and funds **[POLICY-CONFIRM: whether plan funds can support providers' FFS participation for non-members]**.
- **Risks:** inconsistent evidence on rates; rewards enrollment, not acceptance; fairness to providers who already see Medi-Cal.
- **Measurement:** enrollment, new-patient acceptance and billing volume, with payment-lag tracking.
- **View:** administrative support (a billing help desk, claims troubleshooting) looks better supported than bonuses in the short run.

### 8. Community healthcare partnerships (C, sometimes B)
- **Mechanism:** use FQHCs, free clinics, CBOs, faith groups and promotores as trusted entry points and referral partners.
- **Evidence:** reliance on safety-net clinics is high (2.3); CHW and promotora evidence is in candidate A below; ActionHealthNYC used safety-net clinic partners. Direct effect of formal partnership agreements: no direct evidence found.
- **Cost:** no direct evidence found; mostly contracts and coordination staff.
- **Time:** MOUs and referral protocols with existing partners are quick; new funding streams are slower.
- **Authority:** IEHP, partners, county.
- **Risks:** partners are themselves stretched and exposed to the same payment changes (S15, slide 19-20); data-sharing agreements.
- **Measurement:** referrals sent, appointments completed within 30 days, partner capacity reported weekly.
- **View:** an enabler for 6, 11, 12 and 14; not separately evidenced.

### 9. Transportation assistance (C)
- **Mechanism:** reduces travel barriers to appointments.
- **Evidence:** Philadelphia RCT (Chaiyachati et al., JAMA Intern Med 2018): 786 Medicaid beneficiaries who were established patients at two internal medicine practices; offered free rideshare vs usual care; missed appointment rate 36.5% vs 36.7% (p=0.96); 26% (85 of 288 reached) used the ride [VERIFIED: S12, 2026-11-02, mirror PDF]. MACPAC analysis of FY2018 T-MSIS: 61.5 million NEMT ride-days, 3.2 million users, $2.6 billion spending, excluding managed-care plan spending; surveyed users said they could not afford transportation, especially in rural areas [VERIFIED: S13 slides, 2026-11-02].
- **Cost:** $2.6 billion / 61.5 million ride-days is about $42 per ride-day [ESTIMATE: arithmetic from S13; FFS only, mixed modes including ambulance and wheelchair, so it is not a cost for ambulatory rides].
- **Time:** depends on benefit rules. A search summary says FFS NEMT needs a physician certification and mileage can be reimbursed if other transport is exhausted; vehicle types listed are ambulance, litter and wheelchair vans, air [UNVERIFIED: S50]. **[POLICY-CONFIRM: whether UIS adults in FFS get non-medical transportation or NEMT, and how rides are booked.]**
- **Authority:** DHCS (FFS benefit), IEHP for its own members until 12/31.
- **Risks:** low uptake and null effect in an urban sample of established patients; the Inland Empire is spread over 27,000+ square miles (S15), so distance matters more there; transportation without an accepting provider helps nobody.
- **Measurement:** ride requests, completion, and appointment attendance vs a comparison.
- **View:** targeted use for remote areas and dialysis, chemotherapy or recurring visits; not a general solution.

### 10. Transition digital twin (A)
- **Mechanism:** a simulation of members, providers and clinics to test scenarios and capacity.
- **Evidence:** no direct evidence found that a digital twin improves access or outcomes in a Medicaid transition. Any value is as a planning aid.
- **Cost / Time:** no direct evidence found; a simple scenario model is feasible by 1/1.
- **Risks:** presents unsupported inputs as outputs; needs the same missing inputs (section 6). Anything that predicts where UIS members live is barred by contract.
- **Measurement:** back-test predicted vs actual January-March 2027 utilization and provider load.
- **View:** category A, not an access intervention. Its main use is to carry the uncertainty ranges in section 6.

### Candidate A. Community health workers and promotores (C)
- **Evidence:** IMPaCT (S7, S8): see item 6. The Health Affairs economic analysis (302 patients) found a $2.47 return per $1 (range $1.84 to $3.09) from Medicaid inpatient savings; the underlying hospitalization difference was not statistically significant (31.6% control vs 23.3% intervention, p=0.11; admissions 0.64 vs 0.45 per patient-year, p=0.17), the study population was a high-risk, highly structured Philadelphia program, and the return depends on avoided admissions [VERIFIED: S7]. Latino diabetes literature: reviews of CHW RCTs reported HbA1c improvement in about 7 of 12 and 6 of 8 studies, small single-site trials [UNVERIFIED: S38].
- **Cost:** see item 6. Medi-Cal billing: a DHCS example implies about $12.66 per 15-minute unit; an advocacy report says organizations can bill about $26 per half hour, too little to cover overhead, and uptake is limited for community organizations that lack billing capacity [UNVERIFIED: S36]. SPA 25-0016 set an FFS methodology effective April 1, 2025 **[POLICY-CONFIRM: whether it applies to UIS members in FFS]**.
- **Time:** train-and-deploy of new CHWs: weeks to months; using existing promotores in partner organizations is faster.
- **Risks:** trust is also the intervention's strength; low pay and billing gaps.
- **View:** supported for high-risk members in the medium term; not as a 60-day capacity fix.

### Candidate B. FQHC capacity (extended hours, group visits) as primary absorber (B)
- **Evidence:** see 2.4. Reliance is strong; absorption capacity and finance are unknown; group visit and extended-hours effects on new-patient absorption: no direct evidence found.
- **View:** an absorber for existing FQHC patients and partners, but evidence does not support treating FQHCs as the primary absorber for the whole moving group. The student guide itself notes FFS enrollment is a best case.

### Candidate C. Provider-enrollment concierge / fast-track (C)
- Same as item 2. No effect-size evidence. Mechanism is plausible because DHCS states complete applications process faster (S34, UNVERIFIED). Cost is staff time.

### Candidate D. Complex-care continuity handoffs (warm handoff, record transfer) (C/B)
- **Evidence:** I found no rigorous study of warm handoffs or record transfer during Medicaid plan changes. A state transition-handoff example exists (Oregon memo) and generic care-transition toolkits recommend warm handoffs; an uncontrolled readmission observation exists [UNVERIFIED: S51]. Medi-Cal Rx and NC show the failure modes (S23, S24).
- **Cost / Time:** care-manager hours; feasible by 1/1 for a limited list. **Authority:** IEHP before 12/31. **[POLICY-CONFIRM: record transfer, consent, and whether DHCS or FFS providers can receive plan care plans.]**
- **View:** low-regret on logic, thin on evidence.

### Candidate E. Language-concordant scheduling (C)
- **Evidence:** a systematic review of 33 studies reported at least one outcome better with language-concordant care in 25 (76%), no difference in 5 (15%); most were observational (4 RCTs) and none standardized clinician language proficiency [UNVERIFIED: S37, search summary of Diamond et al., J Gen Intern Med 2019]. Another review found mixed results [UNVERIFIED]. In the Inland Empire, half the population is Latino but only 1 in 10 physicians and under one-third of other providers are [VERIFIED: S15, slide 15]. 39% of California FQHC patients have limited English proficiency (S18).
- **Cost:** no direct evidence found. **Time:** feasible if directory language data are accurate. **Risks:** self-reported language skill; **[POLICY-CONFIRM]** interpreter reimbursement in FFS.
- **View:** low-cost and plausibly useful; causal size unknown.

### Candidate F. Pharmacy-based care (B)
- **Evidence:** no Medicaid outcome trial found. California AB 1114 (2016) made pharmacist services (hormonal contraception, immunizations, tobacco cessation, travel medications, naloxone) a Medi-Cal managed care benefit when delivered in outpatient pharmacy; pharmacists must enroll as ORP providers [UNVERIFIED: S52, search summary]. Pharmacy benefits for all Medi-Cal members have been FFS since 1/1/2022 via Medi-Cal Rx (S23), so the pharmacy channel is not newly changed on 1/1/2027. **[POLICY-CONFIRM: whether pharmacist services under AB 1114 are payable to FFS beneficiaries.]**
- **View:** useful for a narrow list of services; not a primary care substitute.

### Candidate G. eConsult for specialty access (B/C)
- **Evidence:** NYC Health + Hospitals, 19 specialty clinics, 50,260 referrals, interrupted time series without a control group: 13% of requests resolved without a visit; among requests needing a visit, appointment scheduled 66.5% to 82.3%; adjusted wait fell 8.2 days (13.3%) from about 61 days; completion of a specialist visit within 90 days unchanged (38.4% vs 37.9%); referral volume fell about 12% (2,228 to 1,961 a month); no cost data [VERIFIED: S14, 2026-11-02]. A Los Angeles County program reported ENT wait falling from 72 to 44 days [UNVERIFIED: S53, trade-press summary].
- **Time:** requires a platform, trained specialist reviewers, and payment; partial pilot with an existing provider organization is the realistic scope by 1/1. **Authority:** provider organizations. **[POLICY-CONFIRM: FFS payment for eConsult codes.]**
- **Risks:** shifts work to PCPs, reviewers may disengage.
- **View:** supported as a specialty access lever in safety-net settings; specialty supply for moved members is the weakest area in the audit evidence (psychiatry 37% accept Medi-Cal, S26).

### Candidate H. Specialty referral pathways (B/C)
- **Evidence:** same as eConsult plus ActionHealthNYC. Dedicated referral agreements with specialists or hospital clinics for transitioning members: no direct evidence found.
- **View:** pair with the high-risk list in item 6.

### Candidates the evidence suggests adding
- **I. Verified availability layer (call-based verification of new-patient acceptance).** Justified by 2.2: directory error rates of 22 to 41% in some plan segments (S4), 49% appointment offering in OIG's sample (S2). Cost: staff or vendor calls, no direct evidence found. Time: a sample-based version can run in November. This feeds items 1, 3, 6.
- **J. Trust and communications design.** Justified by 2.3. Use known senders, avoid collecting immigration information, state what data go where. Effect size of such messaging in this population: no direct evidence found.
- **K. Prompt-payment and claims-support help desk for newly enrolled providers.** Justified by S25 and S26.
- **L. Interim "bridge" pathway** (FQHC and county clinic slots reserved for high-risk movers in January). No evidence found; extrapolated from Medi-Cal Rx emergency-fill practice.

---

## 5. Cross-cutting risks for the immigrant population

- **Visibility risk.** Events, vans and mailed notices that carry a "UIS" label are exposed. Mobile attendance fell 15 to 36% in 2025 (S21).
- **Data-sharing fear.** 51% of immigrant adults, 78% of likely undocumented adults, worry providers will share status information (S16). A June 2025 report that CMS shared Medi-Cal data with ICE is described in S22 (news) [VERIFIED as reported by S22; underlying source not read].
- **State-policy overlay.** Reports describe the enrollment freeze for undocumented adults (1/1/2026), dental benefit end (July 2026), and premiums in July 2027, with premium amounts stated differently by sources ($30 in S16, $50 in S22) **[POLICY-CONFIRM]**. These change who is a "moving member" and how much trust is available.
- **Adults vs children.** The student guide names children and older adults as at risk. The moving group appears to be adults, so child-focused protections may be mismatched **[POLICY-CONFIRM: age range of the moving group]**.

---

## 6. Preliminary view

**Could matter by 1/1/2027 (existing authority, low capital, lower lead time):**
- Targeted provider-enrollment help for high-volume providers, with a hard internal cutoff set by the real PAVE turnaround.
- A verified availability list (sample plus focused calls).
- A risk-stratified handoff list with named enrolled providers, medication supply and care-plan transfer for the highest-need members.
- FQHC and county-clinic partnership agreements for the first 90 days, and language-concordant booking.
- Existing telehealth (audio-first) and eConsult pilots with a willing provider organization.
- Trust-centered communications.

**Probably only later:** mobile clinic fleet, new CHW cohorts at scale, AI/ML matching, a transition-wide eConsult platform, any rate change, digital twin beyond a simple scenario model, new transportation contracts.

**Assumptions in the original list that look wrong or weak**
1. "Enrolled FFS provider" as capacity. See 2.2.
2. Gap mapping and the digital twin as interventions. They are planning aids.
3. AI matching as access creation. It redistributes; the data layer limits it.
4. Mobile clinics as a major absorber: about 3,000 to 4,000 visits per van-year and exposure to chilling.
5. Transportation as a broad fix: the one trial found no effect in an urban sample.
6. Telehealth as a general substitute: Medi-Cal and limited-English users use it less.
7. Financial incentives as quick: rates are not a window lever; evidence on bonuses is absent.
8. FQHCs as the primary absorber: no capacity evidence, and payment for UIS services may change.
9. Pediatric framing: the moving group appears to be adults.

**What cannot be supported**
- Any claim that a listed intervention will cut ED use, deaths or cost for this population by a stated percentage.
- The 36:1 mobile clinic ROI and the 2.47:1 CHW ROI as predictions for this setting.
- Any numeric FQHC "headroom" or panel-size cap taken from the literature.
- A claim about how 2024 plan-transition members fared (no outcome data found).

**The three evidence gaps that most limit a financial model**
1. **Effective FFS supply.** What share of FFS-enrolled Inland Empire providers accept new FFS UIS patients, how many they will take, and how many Group B providers will convert by 12/31. No audit of FFS lists exists; managed-care audit ranges (40 to 65%) and the 25/86 concentration are proxies.
2. **Who moves and what they use.** The Inland Empire number of moving adults, their baseline visits, their current providers' overlap with FFS (Groups A, B, C), and risk mix are not public. The student guide's 10%, 14%, 18% scenarios are assumptions.
3. **Behavioral response and the cost of disruption.** No managed-care-to-FFS study exists, and chilling effects (enrollment loss, avoided care) are changing monthly. Without this, a model cannot say how many members will seek care, delay it, or use the ED, nor what any intervention is worth in the first 90 days.

---

## 7. Sources

All retrieved 2026-11-02. Read status key at top.

| ID | Source | URL | Type | Read |
|---|---|---|---|---|
| S1 | Ludomirsky et al., Health Aff 2022;41(5):760-768, abstract | https://pubmed.ncbi.nlm.nih.gov/35500192/ | primary (abstract) | R-fetch |
| S2 | HHS OIG OEI-02-13-00670, Dec 2014 | https://oig.hhs.gov/oei/reports/oei-02-13-00670.asp | primary | R-fetch |
| S3 | California Healthline summary of S2 | https://californiahealthline.org/morning-breakout/half-of-listed-medicaid-doctors-unavailable-oig-report-finds | secondary | R-fetch |
| S4 | TechTarget report of 2026 OIG maternal-health directory findings (OIG report not opened; a report number OEI-05-24-00090 appeared in a search result and I did not confirm it is the same report) | https://www.techtarget.com/healthcarepayers/news/366644873/OIG-Medicaid-managed-care-provider-directories-have-inaccuracies | secondary | R-fetch |
| S5 | Candon et al., JAMA Intern Med 2018 research letter | https://jamanetwork.com/journals/jamainternalmedicine/article-abstract/2605525 | primary | R-fetch |
| S6 | Polsky et al., NEJM 2015;372:537-545 (DOI 10.1056/NEJMsa1414566 per search summary); related Candon fee-decline paper | not opened | primary | SNIP |
| S7 | Kangovi et al., Health Aff 2020;39(2):207-213 (IMPaCT economics) | https://www.ncdhhs.gov/hlthaff-2019-00981-1/open (host copy of the PDF) | primary | R-local |
| S8 | Kangovi et al., JAMA Intern Med 2018 (IMPaCT RCT) | https://pmc.ncbi.nlm.nih.gov/articles/PMC6469661 | primary | R-fetch |
| S9 | Oriol et al., BMC Med 2009;7:27 (Family Van ROI) | https://pmc.ncbi.nlm.nih.gov/articles/PMC2697174 | primary (model) | R-fetch |
| S10 | Attipoe-Dorcoo et al., J Prim Care Community Health 2020 (mobile clinic costs) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7758644 | primary | R-fetch |
| S11 | Yu et al. 2017 mobile clinic literature review | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5629787/ | primary | SNIP (fetch hit a reCAPTCHA page) |
| S12 | Chaiyachati et al., JAMA Intern Med 2018 (rideshare RCT), mirror copy | https://www.gwern.net/doc/sociology/technology/2018-chaiyachati.pdf | primary (mirror) | R-local |
| S13 | MACPAC NEMT mandated report slides, Jan 29 2021 | https://www.macpac.gov/wp-content/uploads/2021/01/Mandated-Report-on-Non-Emergency-Medical-Transportation-Further-Findings.pdf | primary | R-local (partial) |
| S14 | NYC Health + Hospitals eConsult study (JAMA Health Forum 2021 per search summary) | https://pmc.ncbi.nlm.nih.gov/articles/PMC8796905 | primary | R-fetch |
| S15 | CHCF Inland Empire Regional Market Report slides, June 11 2026 | https://www.chcf.org/wp-content/uploads/2026/06/InlandEmpireRMR2026_Slides.pdf | primary slides | R-local |
| S16 | KFF, Key Facts on Health Coverage of Immigrants | https://www.kff.org/medicaid/fact-sheet/health-coverage-for-immigrants | secondary | R-fetch |
| S17 | KFF, Community health center patients, services, financing (UDS 2025) | https://www.kff.org/medicaid/issue-brief/recent-trends-in-community-health-center-patients-services-and-financing/ | secondary | R-fetch |
| S18 | HRSA UDS, California | https://data.hrsa.gov/topics/healthcenters/uds/overview/state/CA | primary data | R-fetch |
| S19 | NACHC, California fact sheet (2022 UDS) | https://nachc.org/nachc-content/uploads/2024/02/StateFactSheet_CA_2022UDS_Feb2024.pdf | secondary (advocacy) | R-local |
| S20 | UCLA LPPI, Medi-Cal Enrollment Declines Amid Heightened Immigration Enforcement, July 3 2026 | https://latino.ucla.edu/wp-content/uploads/2026/06/Medi-Cal-Enrollment-Declines-Amid-Heightened-Immigration-Enforcement-in-California-.pdf | primary | R-local |
| S21 | CalMatters, Dec 2025, immigrant farmworker clinics | https://calmatters.org/economy/2025/12/immigrant-farmworker-medical-clinic/ | secondary | R-fetch |
| S22 | KVPR / Public Health Watch, May 26 2026 | https://www.kvpr.org/health/2026-05-26/when-new-california-laws-kicked-in-thousands-of-immigrants-dropped-or-lost-medicaid-coverage | secondary | R-fetch |
| S23 | KFF Health News, Feb 9 2022, Medi-Cal Rx | https://kffhealthnews.org/news/article/california-medicaid-patients-struggle-to-fill-prescriptions-medi-cal-rx/ | secondary | R-fetch |
| S24 | Wake Forest press release on NC transition studies (Hanchate et al., J Gen Intern Med; Zimmer et al., NC Med J) | https://newsroom.wakehealth.edu/news-releases/2023/08/research-explores-patient-experience-of-north-carolinas-medicaid-transition | secondary | R-fetch; journal papers not opened |
| S25 | NBER digest of Dunn et al., WP 29010 | https://www.nber.org/digest-202112/administrative-burdens-lead-some-doctors-avoid-medicaid-patients | secondary | R-fetch |
| S26 | California Health Report on the 2015 UCSF/CHCF physician survey | https://www.calhealthreport.org/2016/10/21/fewer-california-doctors-accept-medi-cal-despite-surge-in-number-of-patients/ | secondary | R-fetch |
| S27 | KFF, Medicaid-to-Medicare fee index | https://www.kff.org/medicaid/state-indicator/medicaid-to-medicare-fee-index | primary data page | R-fetch |
| S28 | CHCF, Telehealth Use and Experiences Among California Adults, Sept 2023 (CHIS 2021) | https://www.chcf.org/wp-content/uploads/2023/09/TelehealthUseExperiences-Adults.pdf | primary | R-local (first pages) |
| S29 | CHCF, Lessons from Medi-Cal unwinding | https://www.chcf.org/resource/lessons-medi-cal-unwinding-enrollee-experiences-renewals/ | secondary | R-fetch |
| S30 | Sabety et al., AER: Insights 2023;5(3):327-46 (ActionHealthNYC); NBER w29838 | https://ideas.repec.org/a/aea/aerins/v5y2023i3p327-46.html | primary (abstract) | R-fetch; NBER paper not opened |
| S31 | Altschuler et al., Ann Fam Med 2012;10(5):396-400 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3438206 | primary | SNIP |
| S32 | Housden et al., CMAJ 2013;185:E635 | https://www.cmaj.ca/content/185/13/E635.short | primary | SNIP |
| S33 | California State Auditor 2023-115, 2014-134 | https://information.auditor.ca.gov/reports/2023-115/index.html | primary | SNIP |
| S34 | PAVE processing times (CMA news pages, DHCS bulletins in search results) | https://www.cmadocs.org/newsroom/news/view/ArticleId/35343/Medi-Cal-provider-enrollment-moving-exclusively-to-PAVE-starting-March-5 | secondary | SNIP |
| S35 | DHCS FQHC PPS postponement notice; CPCA financial impact report page | https://www.dhcs.ca.gov/vi/file/fqhc-pn-addendum-three/ ; https://cpca.org/?p=1984 | primary / secondary | notice BLOCKED (empty); CPCA page R-fetch, no figures |
| S36 | CBC report on CHW billing; DHCS SPA 25-0016 | https://calbudgetcenter.org/resources/trusted-but-undervalued-community-health-workers-representatives-promotoras/ | secondary | SNIP |
| S37 | Diamond et al., J Gen Intern Med 2019 (language concordance) | https://pubmed.ncbi.nlm.nih.gov/31147980/ | primary | SNIP (PubMed returned a cookie notice) |
| S38 | CHW/promotora diabetes reviews (search results; mapping of URL to citation not confirmed) | https://pmc.ncbi.nlm.nih.gov/articles/PMC3938962 | primary | SNIP |
| S39 | Urban/CHCF public charge survey 2019; UCLA CHPR | https://www.chcf.org/resource/one-six-california-immigrants-avoid-public-benefits-study-finds/ ; https://healthpolicy.ucla.edu/node/950 | primary | SNIP |
| S40 | Backus et al. 2001 (California physician acceptance); MACPAC 2025 payment review | https://pmc.ncbi.nlm.nih.gov/articles/PMC1495304 (mapping unconfirmed) ; https://macpac.gov/wp-content/uploads/2025/01/Evaluating-the-Effects-of-Medicaid-Payment-Changes-on-Access-to-Physician-Services.pdf | primary | SNIP |
| S41 | DHCS MCP Transition pages and slides; NORC evaluation | https://www.dhcs.ca.gov/MCP-Transition/Pages/Continuity-of-Care.aspx ; https://www.norc.org/research/projects/evaluating-californias-medicaid-managed-care-transition-waiver.html ; CalAIM interim evaluation https://www.dhcs.ca.gov/provgovpart/Documents/CalAIM-1115-Interim-Evaluation-Report-for-the-MCP-Transition.pdf | primary | BLOCKED/empty; SNIP |
| S42 | PPIC, health conditions and care among undocumented immigrants; UCLA CHPR updates | https://www.ppic.org/publication/health-conditions-and-health-care-among-californias-undocumented-immigrants/ | primary | BLOCKED (403) |
| S43 | California Health Report on Denti-Cal participation | https://www.calhealthreport.org/2018/03/28/despite-state-efforts-number-dentists-accept-denti-cal-declined-last-five-years/ | secondary | SNIP |
| S44 | University of Minnesota dissertation on Medicaid plan switching | https://conservancy.umn.edu/items/b1564597-1ed1-4f78-af73-6d8697038864 | primary (thesis) | SNIP |
| S45 | Illinois managed care transition abstracts (APHA; Owen et al.) | https://aphanew.confex.com/apha/143am/webprogram/Paper332334.html | primary (abstract) | SNIP |
| S46 | Health Affairs 2014 SPD managed care experience (title) | https://www.healthaffairs.org/doi/10.1377/hlthaff.2014.0528 | primary | SNIP (title only) |
| S47 | 2SFCA literature (McGrail 2012 and others) | https://pmc.ncbi.nlm.nih.gov/articles/PMC3520708 | primary | SNIP |
| S48 | Vendor/payer AI matching materials (Lyra, Stellation, UnitedHealthcare) | https://www.lyrahealth.com/announcement/lyra-health-study-finds-ai-can-reduce-mental-health-care-costs-without-sacrificing-outcomes/ | vendor | SNIP |
| S49 | JAMA Netw Open LEP video-visit analysis; UCLA CHPR telehealth work | https://healthpolicy.ucla.edu/our-work/publications/telehealth-experience-among-patients-limited-english-proficiency-jama-network-open | primary | SNIP |
| S50 | DHCS Medi-Cal transportation FAQ | https://www.dhcs.ca.gov/services/medi-cal/Pages/Transportation_Beneficiaries_FAQ.aspx | primary | SNIP |
| S51 | Oregon transition warm-handoff memo; Alberta toolkit | https://www.oregon.gov/oha/HSD/OHP/Announcements/Care-Coordination1026.pdf | primary | SNIP |
| S52 | AB 1114 pharmacist services (DHCS ISOR and advocacy blog) | https://www.dhcs.ca.gov/formsandpubs/laws/Documents/DHCS-19-002-ISOR.pdf | primary | SNIP |
| S53 | Healthcare Finance News on LA County eConsult | https://www.healthcarefinancenews.com/news/electronic-consult-program-helps-los-angeles-county-health-system-slash-wait-times-need | secondary | SNIP |

**Sources I tried and could not use:** DHCS pages (Incapsula bot protection returned an empty page to both curl and WebFetch; I did not attempt to bypass), PubMed pages behind a cookie notice, PMC pages behind a reCAPTCHA, PPIC (403), Commonwealth Fund Corlette table (PDF unreadable to the tool).
