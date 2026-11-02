# Policy verification: what happens on January 1, 2027

Workstream: Policy. Retrieved 2026-11-02 unless stated. Source IDs (S.., U..) are defined in `research/source_register.md`.

**Labels.** Numbers carry `[VERIFIED: source, retrieval date]`, `[ESTIMATE: assumption]` or `[UNVERIFIED]`. Arithmetic on published figures is labeled `[ESTIMATE: arithmetic]`, because this workstream owns no script path. `[UNVERIFIED]` here means it was seen only in a search excerpt or could not be confirmed. In any table with a Source column, or where a source ID follows the statement, unlabeled values are VERIFIED from that source at retrieval date 2026-11-02. Each finding also has a confidence level.

**Contract compliance.** The "By Aid Category" file was not opened. No sub-county figure, proxy or map of UIS members was made. Plan-level figures are not split between counties. No provider-level records appear here.

**Access limit.** DHCS's website blocks automated access. Several key DHCS documents were read through public archive snapshots or plan-hosted copies, and three DHCS decks could not be read at all (U01, U02, U03). See the register.

---

## Summary

1. **The guide says the IEHP count "is not public." That is wrong.** IEHP told its Governing Board on August 10, 2026 that "more than 100,000 IEHP members in the UIS population – about 10% of our membership" will move [VERIFIED: S22, 2026-11-02]. The guide's middle (190,000) and high (238,000) scenarios are well above that.
2. **Children and older adults are in the moving population,** subject to immigration status. There is no age exemption. Lawfully residing children under 21, and lawfully residing pregnant or postpartum people, stay in managed care.
3. **"Group B matters most" is not supported by DHCS's own figures.** Statewide, the larger group is providers who are enrolled in FFS but have not billed recently (about 45,000) rather than providers who are not enrolled (about 20,000).
4. **Standard enrollment processing no longer fits before January 1.** Sixty days remain. The statutory response window is 90 days for physicians and 180 for others. DHCS documents dated the same day disagree on whether a provider must be *approved* by January 1 or only *apply* by then.
5. **There is no continuity-of-care protection.** DHCS states the statute does not apply to this move.
6. **IEHP has no plan relationship after December 31, 2026,** and federal guidance bars these members from capitation rates. Whether IEHP may spend on former members is not settled by anything readable here.
7. **There are two cliffs, not one.** July 1, 2027 brings the end of FQHC/RHC PPS for state-only services, emergency-only dental for many adults, and premiums, on top of January 1.
8. **Competition timing:** IEHP is confirmed as sponsor. Final presentations are November 19, 2026, 17 days away. No public case document, spreadsheet or rubric was found.

---

## 1. Who moves on January 1, 2027

**Confidence: High on the rule. Medium on its application, because the table is a member-facing web page read from an archive copy.**

### Rule
All managed care members with UIS move. A member with UIS is one "whose immigration status does not meet the federal criteria for full-scope Medicaid" (S01 p.10). DHCS's list: undocumented people, some green card holders in the five-year bar, and PRUCOL (S03, S05). Coverage continues if they renew on time (S01, S03).

From January 1, 2027, the group also includes members reclassified by H.R. 1 from October 1, 2026 who are age 21 or older and not pregnant or postpartum. These "QNC" members are not flagged as UIS on eligibility files until January 1, 2027 (S01 pp.13-14).

### By group (S06, status table, archive 2026-10-25)

| Group | January 1, 2027 |
|---|---|
| US citizens | Keep managed care |
| LPR past the 5-year bar or exempt; COFA; Cuban or Haitian entrants | Keep managed care |
| **Youth under 21, lawfully residing** | Keep managed care |
| **Youth under 19, not lawfully residing** | **Move to FFS** |
| **Pregnant or postpartum (365 days), lawfully residing** (CHIPRA 214) | Keep managed care |
| **Pregnant or postpartum, not lawfully residing** | **Move to FFS** |
| LPR in the 5-year bar; refugee; asylee; parolee of a year or more; battered immigrant; T visa holder | Move to FFS if age 21+ and not pregnant |
| Most PRUCOL categories; U visa; DACA; pending T visa | Move to FFS if age 19+ and not pregnant (some PRUCOL categories use 21+) |
| Foster and former foster youth to 26, unless LPR, COFA, Cuban or Haitian | Move to FFS |
| **Adults 60+ including undocumented** | **Not exempt from the move.** Listed as keeping Medi-Cal, with emergency-only dental and no premium from July 2027 |

### Exemptions and special cases
| Group | Treatment | Source |
|---|---|---|
| Children | No age exemption. CCS continues; care outside CCS may move to FFS | S01 p.21 |
| Pregnant or postpartum | Only CHIPRA 214 members stay. Others move and are flagged potentially high urgency if due January to March 2027 | S01 pp.21, 35 |
| Seniors | No exemption. Population includes dementia, SNF, CBAS, IHSS and hospice members | S01 pp.33-35 |
| Duals | **Included.** Disenrolled from Medi-Medi (D-SNP) plans effective January 1, 2027, with a 30-day notice. Reason code 93 | S01 p.24, App. E |
| PACE | **Stay in PACE** | S01 p.22, S05 |
| Foster care (HCPCFC), IHSS-R, HCBS waivers | Program continues. Waiver members must find FFS PCP or specialist if theirs do not accept FFS | S01 pp.22-23 |

### Check against the guide's "children, older adults, and people with complex needs"
**The phrase survives, but it needs precision.**

| Group | In the moving population? | Published size (statewide) |
|---|---|---|
| Children | Yes, if not lawfully residing | 251,000 under 21 of 1.9 million [VERIFIED: S31, 2026-11-02]. 178,190 ages 0-18, or 12.5% of the 1,426,411 full-scope expansion group, March 2026 [VERIFIED: S31, 2026-11-02] |
| Older adults | Yes | 410,855 ages 50+, or 28.8% of that group [VERIFIED: S31, 2026-11-02]. **This is 50+, not 65+.** No 65+ count found |
| Complex needs | Yes, and they lose the most: ECM, Community Supports, CCM, TCS | 16,000+ prioritized high-risk enrollees [VERIFIED: S31, 2026-11-02] |

No Inland Empire age breakdown is published. Applying statewide shares to IEHP's range gives roughly 13,000 to 18,000 under 21 and 29,000 to 40,000 age 50+ [ESTIMATE: S31 statewide shares apply to IEHP's 100,000 to 139,425; the 50+ share comes from the expansion group only and may not match the full population].

The guide attributes the phrase to "the brief." The brief could not be found, so its wording could not be checked.

### Disagreements on scope
| Source | Says | Explanation |
|---|---|---|
| IEHP provider notice, Aug 20, 2026 (S26) | "**adult** IEHP Members" move | Earlier and narrower. Contradicted by DHCS (S06, S13) and dropped in IEHP's Oct 15 notice, which says "IEHP members with UIS" (S27). **Treat as superseded** |
| IEHP public page, updated Aug 13 (S30) | Its table puts "Adults aged 19+, non-pregnant" near the FFS row | Page text lists undocumented, five-year LPR and PRUCOL for the FFS change. The adult phrase appears to describe premiums. Extraction lost the column layout, so this reading is not certain |
| DHCS status table vs DHCS "Changes" page (S06 vs S08) | Table has asylees and parolees keeping full Medi-Cal with a premium after July 2027. Changes page says this group gets only pregnancy and emergency care | **Unresolved within DHCS's own pages.** Do not state either as fact for those categories |

### Is this federally required? The framing is partly overstated.
DHCS says "federal rules require" the FFS move (S04). What CMS actually wrote is narrower:
- Emergency Medicaid for these individuals cannot be paid through capitation, and they may not be included in capitation rates or risk-based contracts (S16).
- **States may still cover state-only services through a "separate and distinct contract and payment" with plans** (S16 p.5).
- CMS's recommended route for emergency Medicaid is FFS, and the enforcement date is January 1, 2027 for calendar-year rating periods (S16).

California moved *all* services rather than carving out emergency care because of "technical and administrative challenges" (S19). DHCS priced a state-only managed care program at $6 billion General Fund a year [VERIFIED: S11, 2026-11-02]. A partial carve-out was proposed and rejected in budget talks (S31). So the move to FFS is a California choice made under federal pressure, with fiscal savings as part of it. It is not a federal command to end all plan involvement. This matters for section 5.

---

## 2. How many: statewide, county and IEHP

**Confidence: High that IEHP published the figure. Medium on its exact value and definition. High that no county UIS count was found.**

### Statewide
| Figure | Definition | Source and date |
|---|---|---|
| "approximately 2 million" | DHCS working figure, repeated since May 2026 | [VERIFIED: S01, S11, 2026-11-02] |
| 1.9 million | Total with UIS who will transition, per DHCS Sept 22 deck | [VERIFIED: S31, 2026-11-02] |
| 1,426,411 | Full-scope expansion only, March 2026. **Subset, not the mover count** | [VERIFIED: S31, 2026-11-02] |
| 2,118,287 | UIS enrolled, Chapman estimate from DHCS data early 2026 | [VERIFIED: S42, 2026-11-02] |
| About 1.88 million | LHPC: 1.6 million in its plans, which cover about 85% | [ESTIMATE: arithmetic on S31 figures] |

The spread reflects date and definition. It is not a real conflict. CHCF describes the gap between 1.4 and 1.9 million as "restricted-scope" enrollees (S31). Restricted-scope enrollees are not a natural managed care population, and the other UIS groups in S06 (for example five-year LPR and PRUCOL) are full-scope, so that label may be imprecise. It could not be checked without U01.

### The guide's denominator
DHCS reports 13,207,633 in plans and 702,547 in FFS in April 2026, or 13,910,180 in total [VERIFIED: S01, 2026-11-02]. The guide's "more than 14 million" is slightly high for April 2026, though CHCF reports 14.5 million for March 2026 on a different count (S31) and the LAO estimates 13.9 million for 2026-27 (S19).

| Ratio | Value |
|---|---|
| 2 million / all Medi-Cal certified eligibles, April 2026 | 14.4% [ESTIMATE: arithmetic] |
| 2 million / managed care members, April 2026 | 15.1% [ESTIMATE: arithmetic] |

DHCS's "2.8-fold increase" (S01 p.15) matches 2 million divided by 702,547, which is 2.85. Total FFS enrollment would rise to about 3.85 times its current size [ESTIMATE: arithmetic]. Use the second figure if describing the size of FFS after the move.

### IEHP
"The transition of more than 100,000 IEHP members in the UIS population – about 10% of our membership" (S22 p.31, August 10, 2026).

**The statement is internally loose.** 100,000 is 7.6% of IEHP Medi-Cal members (1,321,983), while 10% is 132,198 of Medi-Cal members or 139,425 of all members [ESTIMATE: arithmetic]. The published range is therefore about **100,000 to 139,000.**

**Do not confuse this with 370,000.** That is IEHP's count for the work requirement population, on the preceding slide (S22 p.30). A search summary wrongly presented these two as conflicting.

**Open definition issue.** The statement predates DHCS's clarification that QNC members are added to the UIS group only from January 1, 2027. DHCS projects 148,000 such people statewide [VERIFIED: S10, 2026-11-02]. Whether IEHP's figure includes them is unknown. If IEHP holds about 10% of them, in line with its 10.0% share of statewide plan enrollment, that adds about 15,000 [ESTIMATE: proportional share, untested].

**An anomaly worth asking about.** IEHP has 10.0% of statewide plan enrollment but reports only 5% to 7% of the 2 million movers [ESTIMATE: arithmetic]. Yet Riverside ranks fourth and San Bernardino sixth among counties by affected enrollees (S35). Molina and Kaiser members are outside IEHP's figure, and Kaiser and Molina together hold about 20% of plan enrollment in the region at December 2024 (S32). The figures can be reconciled only with data nobody has published. **Ask IEHP directly.**

### County level
**No published count of UIS enrollees for Riverside or San Bernardino was found.** The only county fact is the rank order: "Los Angeles County has the largest number of affected Medi-Cal enrollees, followed by Orange, Santa Clara, Riverside, San Diego and San Bernardino" (S35, reporting DHCS's Sept 30 webinar). San Bernardino County's own notice gives no count (S49). DHCS has said it prioritized "Los Angeles County and Southern California, where the UIS population is most concentrated" (S31).

An older ITUP fact sheet appeared in search results with county undocumented counts for 2022, with a later sheet showing near-zero values. These look like a reporting break, are out of date and were not used.

### Proposed replacement for the guide's scenarios
| Scenario | Members | Share of IEHP Medi-Cal (1,321,983) | Basis |
|---|---|---|---|
| Low | 100,000 | 7.6% | IEHP "more than 100,000" floor [VERIFIED: S22, 2026-11-02] |
| Middle | 132,000 | 10.0% | IEHP "about 10%" of Medi-Cal members [ESTIMATE: IEHP's 10% applied to Medi-Cal row] |
| High | 155,000 | 11.7% | IEHP's 10% of all members (139,425) plus about 15,000 QNC [ESTIMATE: proportional QNC share, may double count] |
| Guide's middle | 190,000 | 14.3% | Statewide ratio. **Not supported for IEHP** |
| Guide's high | 238,000 | 18% | Illustrative only. **Not supported for IEHP** |

The guide's own low of about 132,000 now becomes the middle. Whether to keep the guide's scenarios for comparison is an owner decision. The figures may shrink through 2027 (section 8).

---

## 3. What FFS enrollment requires, and can it be done in time

**Confidence: High on the requirement and published time limits. Low on what happens to an application pending on January 1, because DHCS's documents conflict.**

### Requirement
- Being in an MCP network "does not carry forward, only enrollment in Medi-Cal FFS does" (S04). A plan contract does not satisfy enrollment (S14 Q10).
- New providers apply through PAVE. Each individual needs a unique profile and must sign personally (S04, S14 Q13).
- Individuals pay no application fee. The $750 fee does not apply to them (S14 Q12) [VERIFIED: S14, 2026-11-02].
- Non-PAVE routes exist: CBAS centers enroll through the Department of Aging (S01 p.65).
- Transportation providers must also enroll in FFS (S04).

### Processing time
| Applicant | Published limit | Source |
|---|---|---|
| Physicians and physician groups | 90 days, then provisional status from the 91st day if no notice | [VERIFIED: S40, S14, 2026-11-02] |
| All other applicants | 180 days, then provisional status from the 181st day | [VERIFIED: S40, S14, 2026-11-02] |
| Notices to providers | "up to 90-180 days" | [VERIFIED: S15, S29, 2026-11-02] |
| CMA, for physicians | "up to 90 days" | [VERIFIED: S35, 2026-11-02] |
| Provisional status | 12 months | [VERIFIED: S40, 2026-11-02] |
| Preferred provisional, physicians meeting criteria | Up to 18 months, considered within 90 days | [VERIFIED: S40, 2026-11-02] |

The 90 and 180 day figures are legal maximums before provisional status. Actual current PAVE processing times and any backlog were **not established**. Incomplete applications take longer (S14 Q15).

### The arithmetic as of today, November 2, 2026
- 60 days remain until January 1, 2027 [ESTIMATE: arithmetic].
- To have the full statutory window run by January 1, a physician needed to apply by October 3, 2026, and other applicants by July 5, 2026 [ESTIMATE: arithmetic].
- A physician applying today has a response window to January 31, 2027. Other applicants have until May 1, 2027 [ESTIMATE: arithmetic].

**Answer: an application can be filed in time, but approval in time cannot be counted on.**

### Expedited path
**None found.** No DHCS document read describes faster PAVE processing or a provisional status created for this transition. DHCS's only transition-specific speed-up is for authorizations (TAR special handling), not enrollment. Absence from what could be read is not proof, since U01 to U03 are unread.

### The central conflict: approved by, or submitted by?
| Source | Date | Wording |
|---|---|---|
| Policy Guide v3.0, Appendix B template (S01 p.70) | 2026-10-14 | "must submit an application and be **approved** for enrollment by January 1, 2027" |
| Provider Toolkit v1.0 (S04 p.5) | 2026-10-14 | "must **submit** your application by January 1, 2027 to bill for these members" |
| IEHP notice (S27); Alameda Alliance (S44) | 2026-10-15; 2026-08-17 | "apply and be approved" |
| Provider FAQ (S03) | Sept 2026 | "will not be able to care for UIS members after December 31, 2026" |

Both DHCS documents carry the same date. The Medi-Cal enrollment FAQ adds a possible reconciliation: "In most cases, the effective date is the date the application is received," and one year earlier for ORP (S14 Q3). If that rule applies, a provider who applies before seeing the patient might later be paid for those visits once approved. **This is an inference, not a DHCS statement about this transition.** A provider is unlikely to rely on it without written confirmation.

**Action: a question to DHCS's Provider Enrollment Division would settle this.** Until then, do not state either version as fact.

### Group B is the smaller problem
At DHCS's September 30 webinar (S35, CMA's report of it; primary deck U02 unread):

| Providers serving affected patients, statewide | Count | Share |
|---|---|---|
| Managed care providers serving affected patients | about 151,000 | 100% |
| Enrolled in FFS but not billing recently | about 45,000 | 30% |
| Not enrolled in FFS | about 20,000 | 13% |
| Remainder | about 86,000 | 57% |

[VERIFIED: S35, 2026-11-02; shares ESTIMATE: arithmetic]

DHCS defines the at-risk provider as one it "cannot confirm" is enrolled or that has "not submitted any Medi-Cal FFS claims in the last 12 months" (S01 p.31). For enrollees rather than providers, 58.7% of those in active treatment (751,853 of 1,281,401) have providers not billing FFS [VERIFIED: S31, 2026-11-02]. CHCF says these providers "cannot be paid ... unless they enroll," which overstates it, since some of them are enrolled but dormant.

**Further limits on "enrolled means available":**
- "Accepting new patients is a choice" (S04).
- ORP-only enrollment satisfies the prescriber rule but does not pay for directly furnished services (S14; U11). Prescribers have been pushed to enroll since early 2026, so the enrolled file may include people who cannot bill for visits. **The data workstream should test whether Source E separates ORP records.**
- A provider may bill FFS under a different NPI from the plan's (S01 p.31).
- Prescriber enforcement slipped: DHCS first set June 26, 2026 (S15), but IEHP said on October 1 that it will begin "soon" with no date (S29).

---

## 4. Continuity of care and notices

**Confidence: High.**

### Continuity of care
**No statutory protection applies.** "Statutory continuity of care requirements applicable to MCPs under California law do not apply here" (S01 p.26). Health and Safety Code 1373.96 "does not apply to Members transitioning from managed care to Medi-Cal FFS" (S01 fn.4). The transition-of-care tools below are DHCS policy for plans, and access is preserved only "to the extent the Provider is enrolled in Medi-Cal FFS" (S01 p.26).

### Members mid-treatment
| Situation | Provision | Source |
|---|---|---|
| Inpatient on Dec 31 and Jan 1 | Plans report them to DHCS. Plans must honor network agreements, which may cover the full stay. "In no circumstance will the Member be balance billed" | S01 p.28 |
| Existing authorization | **TAR special handling:** FFS provider still files an eTAR but needs no attachments if DHCS has the plan's authorization. DHCS accepts TARs from Nov 1, 2026 for services from Jan 1, 2027 | S01 pp.27-28, S04 |
| Authorization received before Jan 1 for later services | Plan may process it or refer the provider to DHCS | S01 p.28 |
| Long-term care | Facilities may not transfer or discharge because of the coverage change (42 CFR 483.15) | S01 p.63 |
| One-time DME, CCS whole-child model only | Delivered by Dec 1. Plan pays if authorized by Dec 31 even if delivered later. **Riverside and San Bernardino's CCS model was not confirmed here** | S01 p.48 |
| Prescriptions | Refill before Jan 1. IEHP recommends 90-day prescriptions with four refills where appropriate, because members "may not have access to a provider who can prescribe" | S01, S27 |
| High urgency | Special population **and** anticipated service gap. Includes dialysis, chemotherapy, radiation, transplant, dementia, home health, life-sustaining DME, seizure and blood disorders, and births due Jan to Mar 2027 | S01 pp.30-36 |
| Referrals Oct 1 to Dec 31 | DHCS "requests" that PCPs refer to providers also enrolled in FFS, when possible | S01 p.59 |

CHCF notes DHCS "does not guarantee" that authorization transfers finish by January 1 and calls for honoring authorizations for a defined period after it (S31). No such guarantee exists in what was read.

### Plan duties and dates
| Date | Duty |
|---|---|
| Oct 2026 | DHCS sends member registries including high urgency flags; outreach starts on receipt (S01 p.30) |
| Nov 6 | Contact data and mid-point high urgency dispositions due (S01 Table 4) |
| Nov 15 | PCP, ECM, CCM and CBAS provider notices due; plans direct care managers to start transition support (S01 pp.57-60, 65) |
| Dec 1 | Members expected to have the DHCS notice; CCS and D-SNP notices due (S01 pp.37, 39, 81) |
| Dec 1-10 | DHCS provider trainings (S01 Table 10) |
| Dec 7 | Final dispositions; NEMT and NMT schedule file (S01 Table 4) |
| Dec 31 | Plan care coordination and warm handoffs end (S01 p.26) |
| To Jan 29, 2027 | Authorization, at-risk and care plan files continue (S01 Table 4) |

### Notices and support
- **One** mailed DHCS notice, in 19 languages, with additional information by QR code. Texts in October, November and December (S01 pp.37, 42). San Bernardino County describes a further December notice (S49).
- No new BIC cards are issued (S01 p.38).
- From January, a Nurse Advice Line and care coordinators; a statewide vendor is being contracted (S01 p.29). $39 million General Fund in 2026-27 [VERIFIED: S10, 2026-11-02], split $31 million for care coordination and $8 million for navigators [VERIFIED: S31, 2026-11-02]. Relative to about 2 million people, that is about $20 per person [ESTIMATE: arithmetic].
- From January 1, the Medi-Cal Helpline is the main intake. It runs weekdays 8 to 5. Secondary pathways are still to come (S01 p.53).
- There is no FFS equivalent of the Member Handbook (S01 p.41). No FFS network adequacy standards (S31).

---

## 5. What IEHP may do for people who have left its plan

**Confidence: High on what ends. Low on what IEHP may spend on former members. This is research, not legal advice. Items marked "open" need counsel or DHCS.**

### Member relationship
**None after December 31, 2026.** "IEHP coverage will end for impacted Members" (S28). "You will not be in a Medi-Cal health plan anymore" (S05). DualChoice members also leave (S01 p.24). The only continuing duties found are the wind-down items in section 4. "IEHP remains deeply committed to serving the UIS population" (S22) is a statement of intent, not an authority.

### Capitation
**IEHP loses it.** Federal guidance bars these individuals from "capitation rates, the capitation payments that states pay to managed care plans, or risk-based contracts," and rate certifications and directed payment preprints must exclude their data (S16). No published dollar figure for IEHP was found. Two rough bounds:

| Basis | Per member per year | 100,000 members | 139,425 members |
|---|---|---|---|
| IEHP Medi-Cal average, June 2026: $630.7M on 1,374,807 member months, about $459 per month | about $5,505 | about $551M | about $768M |
| DHCS price of state-only managed care: $6B over 1.9M to 2M people | $3,000 to $3,158 | about $300M to $316M | about $418M to $440M |

[ESTIMATE: gross revenue only. Assumes UIS members match these averages, which they do not. The average includes long-term care and other high-cost groups.]

**Gross revenue is not the loss.** Medical costs leave as well. In June 2026, IEHP Medi-Cal medical costs were 89% of revenue and G&A was 3.8% [ESTIMATE: arithmetic on S22]. IEHP also already returns money under a UIS risk corridor: about $21 million for 2025 per its auditors (S23), with the corridor continuing in 2026 (S25). DHCS says utilization among UIS enrollees has been below projections (S19). So margin on this group may already be thin. PCPs also lose capitation and P4P on these members, as they do for lapsed members (S25), which is an inference for this group.

### What IEHP can and cannot do

| Action | Status | Basis |
|---|---|---|
| **Before Jan 1:** outreach, PAVE encouragement, provider surveys, warm handoffs, referrals to FFS-enrolled providers, data files to DHCS | **Required or expected** | S01; IEHP is doing this (S27, S28) |
| Member communications using DHCS material | **Allowed,** file and use | S01 p.37 |
| Care plans and handoffs by plan care managers | **Required** to Dec 31 | S01 |
| Connecting members to local resources | **Encouraged,** while stating these may not be Medi-Cal covered | S01 p.40 |
| Plan covering or paying for Medi-Cal services after Jan 1 | **No basis.** "Medi-Cal FFS will assume responsibility" except inpatient and agreement-based carry-overs | S01 p.28 |
| ECM or Community Supports as a Medi-Cal benefit after Jan 1 | **Not possible.** Not covered in FFS | S01 pp.18, 25 |
| Using PHI for its own operations, or disclosing to another covered entity for care coordination about a former member | **Permitted in principle.** Disclosure applies where each entity "either has or had a relationship" with the person. Limited purposes, and minimum necessary still applies | S41 |
| Treating the UIS flag casually | **Not allowed.** "The UIS indicator is protected health information" and must be handled under HIPAA and the CMIA "with the same level of sensitivity" | S01 p.43 |
| Using capitation revenue to pay for non-members' care | **Open, and looks risky.** CMS's stated concern is that "Medicaid is cross subsidizing state-only programs," and state-only funding must use a separate contract (S16). Whether this reaches a plan's discretionary spending of surplus is not addressed. | S16 |
| A separate state-only contract with IEHP | **Federally allowed, not funded.** California chose not to do this (S11, S31) | S16 |
| Community Reinvestment funds | **Possibly the best vehicle; open.** Plans must reinvest part of Medi-Cal net income locally. IEHP accrued about $22 million through March 2026 [VERIFIED: S24, 2026-11-02]. Excerpts say it serves "communities in which the MCP operates," must tie to community needs, and cannot fund what the MCP contract already covers [UNVERIFIED: U07, U08]. Whether non-members qualify was **not established** | S24, U07, U08 |
| Reserves | **Constrained.** IEHP reports a recovery after "significant losses" in 2024 and aims to "build back up our reserves"; DMHC still requires monthly reporting (S22). TNE chart values extract as 383% to 449% with 33 to 48 days cash, but the month labels are not machine-readable, so verify by eye [VERIFIED: S22, 2026-11-02]. Consolidated surplus about $219M through June 2026 [VERIFIED: S22, 2026-11-02]. Gift-of-public-funds and DMHC limits for a public plan were **not researched** | S22 |
| Provider payments to Medi-Cal FFS providers on top of state rates | **Open.** Nothing read allows or forbids it | none |
| IEHP as navigator or care coordination contractor | **Not established.** The statewide care coordination vendor is unnamed. The $8M navigator program reportedly runs through CPCA with 28 to 45 grantees [UNVERIFIED: U09] | S01, U09 |
| IEHP Community Wellness Centers and ConnectIE serving former members | **Not established.** Website describes them generally; eligibility rules not checked | S30 |
| D-SNP counseling on other Medicare options | **Allowed** to current enrollees, with caution about Medicare loss | S01 App. E |

**Sensitivity note.** CMS has asked California for "all immigration enumerators ... for every Medicaid beneficiary" and is recouping over $1.6 billion in federal funds [VERIFIED: S17, 2026-11-02]. CHCF reports enforcement is making undocumented people reluctant to seek care (S32). Any design that builds a list of former UIS members needs a strong justification and legal review.

---

## 6. FQHC, RHC and Tribal payment, and benefit carve-outs

**Confidence: High on the budget dates and carve-outs. Medium on FQHC mechanics, because the current clinic letters are unread. Low on Tribal treatment.**

### FQHC and RHC payment
| Period | Payment for state-only services to UIS members |
|---|---|
| **Now** | Plan rate plus DHCS "wrap" up to PPS (S12) |
| **Jan 1 to Jun 30, 2027** | FFS, with PPS retained. Elimination delayed "from July 1, 2026 to July 1, 2027" [VERIFIED: S10, S13, S18, 2026-11-02]. The claim mechanics for FFS visits were not published in anything read; FFS guidance was "forthcoming" [UNVERIFIED: U04] |
| **From Jul 1, 2027** | "Applicable Medi-Cal Fee Schedule rate" in FFS, and PPS rates "are typically higher" than that (S12). General Fund effect $1 billion per year [VERIFIED: S10, 2026-11-02] |
| Federally eligible emergency and pregnancy services | Wrap and PPS continue [UNVERIFIED: U04] |

**Correction to CHCF.** The brief says FQHCs and RHCs "will no longer be reimbursed for serving the UIS population beginning July 2027" (S31). DHCS's description is a *rate* change to fee schedule, not an end to payment (S12, S10). Chapman estimates a loss of $906 million to $1.1 billion a year statewide, about 14% of net clinic revenue, on May 2026 assumptions [VERIFIED: S42, 2026-11-02].

**Tribal.** Excerpts from a DHCS public notice exclude IHS/MOA clinics, Tribal FQHCs and Urban Indian Organizations from the change [UNVERIFIED: U06]. This was a 2025-26 notice, and its status in the final letter is unconfirmed.

**In the FFS provider file?** Clinics bill the wrap through DHCS's fiscal intermediary (S12), so FQHCs and RHCs should already be enrolled [ESTIMATE: inference from billing mechanics]. Whether Source E shows them by a distinct provider type should be checked in the data, and individual clinicians within a clinic may appear separately or not at all. **CHW limit:** "non-tribal FQHC and RHC providers may use CHWs ... CHWs are not considered to be FQHC and RHC billable" (S01 fn.14). This limits clinic-based CHW interventions.

### Benefits

| Service | After Jan 1, 2027 | Source |
|---|---|---|
| **Medi-Cal Rx** | Unchanged. But the prescriber must be enrolled under a Type 1 NPI once enforcement starts | S01 p.20, S29 |
| **Specialty mental health, SUD** (county BHP; includes DMC-ODS and DMC where applicable) | Unchanged; same providers. Targeted Case Management continues under conditions | S01 pp.20, 25 |
| **Non-specialty mental health** | **Moves from plan to FFS.** Therapy and counseling from any FFS provider | S01 p.18, S03, S05 |
| **NEMT and NMT** | Covered in FFS. Transport providers must enroll in FFS. May need new authorizations. Plans send scheduled trips by Dec 7. **DHCS deck reportedly warns "86% of rides provided today are through brokers who can't enroll" [UNVERIFIED: U01]. If confirmed, this is a major access risk.** | S01 p.17, S03, S04 |
| **ECM, CICM, Community Supports, CCM, TCS** | **End.** Plans pay through Dec 31 | S01 pp.25, 39 |
| **CHW, doula, dyadic, asthma, CPSP, collaborative care** | Available in FFS. "Do not guarantee Medi-Cal FFS payment for any provider types." Further codes pending | S01 pp.55-56 |
| **Dental** | No change on Jan 1. **Inland Empire is on Dental FFS** ("all other counties"). Emergency-only for many UIS adults from Jul 1, 2027 | S03, S01 p.22 |
| **Vision, DME, home health** | Covered; new FFS authorization may be needed | S01 p.19, S03 |
| **CBAS** | Continues. No PAVE needed | S01 p.65 |
| **PACE, CCS, IHSS-R, HCPCFC, HCBS waivers** | Continue; see section 1 | S01 pp.21-23 |
| **Maintenance dialysis** | State-only coverage from Oct 2026, AB 173, $8M in 2026-27 [VERIFIED: S18, 2026-11-02] | S18 |

---

## 7. FFS vs managed care reimbursement

**Confidence: High on the index values. Medium on current FFS levels. IEHP's contract rates could not be established.**

### Does the guide's fee index hold up?
| KFF index, 2024 | All services | Primary care | Obstetric | Other |
|---|---|---|---|---|
| United States | 0.75 | 0.66 | 0.88 | 0.84 |
| **California** | **0.67** | **0.56** | **0.85** | **0.81** |
| California, 2019 | 0.73 | 0.76 | 0.61 | 0.73 |

[VERIFIED: S34, 2026-11-02]

**The guide's national figures (0.75, 0.66) are correct.** It omits that California is below both. FFS-only data, so it is the right kind of index for this question.

### The 0.56 vs 87.5% conflict
DHCS says 2024 targeted rates raised FFS primary care, maternity and non-specialty mental health to 87.5% of Medicare, with plans required to pay at least that (S20, S31), and funding continues with a new MCO tax through 2029 (S10). KFF shows California primary care at 0.56 in 2024, which cannot both describe the same thing. Possible explanations are survey timing, code mix (the ACA parity codes), or Medicare locality (DHCS's base is reportedly the *lowest* California Medicare locality [UNVERIFIED: search excerpt of DHCS material]). The Urban Institute's methods could not be opened. **This could not be resolved. Cite both with their definitions and do not treat 0.56 as the current floor.** The 2019 to 2024 fall from 0.76 to 0.56 in primary care is also unexplained.

### FFS vs IEHP contract rates
- **IEHP's contract rates are not public** and could not be established. Its board report shows some PCPs on capitation and others labeled "PCP - FFS" (S22). That label means how *IEHP* pays them. It does not mean enrollment in Medi-Cal FFS. **This is a trap for the data work.**
- Best public evidence: a DHCS analysis cited by the LAO in May 2024 found "managed care plans pay higher rates on average" than FFS. The gap was slight for maternity and mental health. Primary care was close to 90% of Medicare, more than 10 points above FFS (S20). This predates or straddles the 2024 increases, so the gap may have narrowed.
- Plans sometimes benchmark to FFS and sometimes capitate groups (S20). Plans warn that FFS rates "may differ" from contract rates (S47), and CMA says FFS schedule replaces "negotiated managed care rates" (S35).
- CHCF reports that "the state estimates a 16% increase in emergency and inpatient care" after the transition [VERIFIED: S31, 2026-11-02]. The figure's sources are listed together with others in the brief, so its origin could not be traced and the DHCS deck U01 was not read. Cite it as CHCF reporting a state estimate.

**Conclusion:** FFS rates are likely somewhat below IEHP's contract rates for many services. The size for IEHP specifically is unknown, and any model input is an assumption.

### Prop 35, MCO tax and the guide's study
- About $300 million a year supports continuing 2024 rate increases, the plan "assumes Prop 35 cannot be implemented as written," and the current MCO tax ends December 31, 2026 [VERIFIED: S18, 2026-11-02]. The new tax needs federal approval, and its net revenue is $2.3 billion a year vs $7.6 billion [VERIFIED: S18, 2026-11-02].
- Prop 35 primary and specialty supplemental payments for July to December 2026 were reportedly pending SPA 26-0029 [UNVERIFIED: U10]. Whether any supplemental reaches UIS FFS visits was not established. CMS bars UIS data from directed payment preprints (S16). End of Prop 56 supplemental payments was also delayed to July 1, 2027 (S13).
- Decker 2012: 69% of physicians accepted new Medicaid patients, and a 10-point rise in the fee ratio raised acceptance by about 4 points (S39) [VERIFIED: S39, 2026-11-02]. California had the second-lowest acceptance rate. The guide's summary is fair, but the data are from 2011, national and cross-sectional, so it does not show a causal effect or estimate today's California response.

---

## 8. Related changes that compound this

**Confidence: High unless noted. All dates checked against DHCS or LAO.**

| Effective | Change | Who | Source |
|---|---|---|---|
| Jan 1, 2026 | **Enrollment freeze** for full-scope | Adults 19+ with UIS. Under 19 and pregnant can still apply. Enrolled people keep it if they renew; those who lapse lose it and cannot re-enroll | S07, S25 |
| Oct 1, 2026 | H.R. 1 narrows qualified non-citizen | 148,000 people statewide projected. State-funded full scope to Jun 30, 2027 | S01, S10, S08 |
| Oct 1, 2026 | Federal match for ACA adult emergency care falls from 90% to 50% | State budget effect | S10 |
| Oct 2026 | State-only maintenance dialysis | Federal emergency funding ends for scheduled dialysis | S18 |
| **Jan 1, 2027** | **FFS move** | This analysis | S01 |
| Jan 1, 2027 | **Work requirements:** 80 hours or $580 a month | ACA adults 19-64 without child under 13; includes immigrants in the new rules. IEHP: about 370,000 members. Litigation filed June 2026 | S08, S09, S22, S30 |
| Jan 1, 2027 | Shorter retroactive coverage | One month for adults 19-64 without children, two for others | S09 |
| Feb 1, 2027 (proposed) | **Medicare ends** for some non-citizens, under the CY2027 PFS proposed rule. Whether final was not checked | Some UIS duals | S01 App. E |
| Mar 1, 2027 | **Six-month renewals** | Expansion adults 19-64; see disagreement below | S08, S09 |
| Jul 1, 2027 | **Premiums:** set at $30; May 2027 revision to set it between $30 and $50. Non-payment means restricted scope | Ages 19-59. Exempt: children, pregnant, foster, 60+ | S07, S10, S18 |
| Jul 1, 2027 | **Dental:** emergency-only. Delayed from Jul 1, 2026 | UIS adults 19+, not pregnant | S10, S01 fn.2 |
| Jul 1, 2027 | **FQHC and RHC PPS ends** for state-only services | Clinics serving UIS members | S10 |
| Jul 1, 2027 | Restricted scope (see section 1 for the DHCS inconsistency) | QNC group | S10, S08 |
| Jul 1, 2027 | Asset limit falls from $130,000 to $21,000 for one person | Age 65+, disability, nursing home, some families | S30 |

### Date disagreements
| Item | Versions | Explanation |
|---|---|---|
| Six-month renewals | March 1, 2027 (S08, S09, S30); "starting in September 2027" for IEHP's group (S22); bundled under January 2027 in S13 | S08 is the latest and most specific. September may be when IEHP expects its first cycle to land. Not confirmed |
| Dental | DHCS FAQ snapshot still says July 1, 2026 (S07) | S07 is stale. July 1, 2027 is law per S10 and S18 |
| Premium amount | $30 (S07), $30 to $50 (S18), "$50 ... subject to a determination" (S10) | Budget deferred the decision to May 2027 |
| Savings | $584M and $1.5B (S11, S31) vs $637M and $1.6B (S10) | May Revision vs enacted budget. General Fund $472M vs $525M |
| Prescriber enforcement | June 26, 2026 (S15) vs "soon" (S29) | Date slipped. No current date found |

**Effect on the numbers.** The moving population is shrinking and will not be a stable denominator. CHCF cites projections that the UIS uninsured rate rises from 25% in 2024 to over 50% by 2030 [VERIFIED: S31, 2026-11-02]. No published estimate of disenrollment caused by the FFS move itself was found. Search summaries attach a figure of "about 30,000" to this move, but in the LAO's text that question sits in its asset-limit discussion (S19), so **do not use 30,000 for the FFS move.**

---

## 9. The guide's numbers and references

**Confidence: High.**

### Values that match
| Guide | Result | Source |
|---|---|---|
| IEHP Medi-Cal 1,321,983; DualChoice 38,185; Covered 34,078; total 1,394,246 | **Match,** and sum correctly | [VERIFIED: S21, 2026-11-02] |
| "Dated October 2026; the count month is not stated" | **Correct.** Board report: 1,393,185 for Aug 2026, 1,399,163 for July [VERIFIED: S22, 2026-11-02] | S21, S22 |
| Riverside 2,544,916; 8.0%; $93,074; 9.8% | **Match** | [VERIFIED: S37, 2026-11-02] |
| San Bernardino 2,224,091; 8.1%; $85,478; 12.6% | **Match** | [VERIFIED: S38, 2026-11-02] |
| "more than two million", "94%" | **Match, with a caveat:** 2,002,437 and 94% are **2024** data, not 2026 [VERIFIED: S32, 2026-11-02] | S32, S33 |
| FAQ quote on Group B | **Exact match** | S03 |
| KFF 0.75 and 0.66 | **Match** | S34 |
| Scenario arithmetic | 132,198; 188,855 (1 in 7); 237,957. **Correct** [ESTIMATE: arithmetic] | |

**IEHP provider network, not quoted in the guide but pointed to:** PCP 1,488; Specialists 2,817; Behavioral Health 3,453; Hospitals 34; Other 2,570; Total 10,362, which sums correctly [VERIFIED: S21, 2026-11-02]. This mixes individuals and facilities, and the "Other" row mixes types. It is **not** comparable with the FFS file's record counts.

### Useful published access figures for the analysis
| Measure (Inland Empire) | Value | California | Source |
|---|---|---|---|
| Physicians per 100,000, 2024 | 229 (64% of state) | 358 | [VERIFIED: S32, 2026-11-02] |
| Physicians working 20+ hours | 200 (68%) | 294 | [VERIFIED: S32, 2026-11-02] |
| Primary care | 85 (72%) | 118 | [VERIFIED: S32, 2026-11-02] |
| Specialty | 115 (65%) | 176 | [VERIFIED: S32, 2026-11-02] |
| Psychiatry | 11 (64%) | 18 | [VERIFIED: S32, 2026-11-02] |
| Behavioral health providers | 300 (78%) | 384 | [VERIFIED: S32, 2026-11-02] |
| Physicians speaking Spanish | 13% | | [VERIFIED: S32, 2026-11-02] |
| **FFS provider records, Sept 25, 2026: Riverside 13,267; San Bernardino 14,781** | | 373,367 total, with 97,279 records lacking a county | [VERIFIED: S31, 2026-11-02] |

Search results also showed a figure of 42 primary care physicians per 100,000 from older press. That uses a different measure, so use CHCF's Table 14.

**Warning for the data workstream.** CHCF's analysis of the FFS file found that **63.7% of records have unknown or not-applicable specialty** and 11.1% have unknown type, statewide [VERIFIED: S31, 2026-11-02]. The guide's step of counting primary care vs specialty providers by ZIP could be badly affected. Test this in the Inland Empire extract.

### Mismatches and errors in the guide
| Location | Problem |
|---|---|
| **Reference numbers** | In-text numbers are off by one from Ref 2 onward. IEHP fact sheet cited as Ref 1 (is 2). FAQ as Ref 2 (is 3). CHCF as Ref 3 (is 4). HPSA as Ref 4 (is 5). Decker as Ref 5 (is 6). KFF as Ref 6 (is 7). Census Ref 1 and CHCF 2020 Ref 8 are right |
| **Section numbers** | Contents lists seven sections. The body has two "Section 2" headings and ends at 6. Later cross-references follow the body numbering |
| §2.2 "not public" | **Wrong** since August 10, 2026 (S22) |
| §2.2 "more than 14 million" | Slightly high for April 2026 (13.91M, S01), depending on source |
| Source D "the other plan in the region" | **Incomplete.** There are three plans: IEHP 79.4% and 78.8%, Molina 11.1% and 10.7%, Kaiser 9.0% and 10.1% by county, Dec 2024 [VERIFIED: S32, 2026-11-02]. The project contract mentions Molina only, so Kaiser should be added |
| "IEHP ... more than 90%" (fact sheet, S21) vs CHCF | Fact sheet's market claim conflicts with CHCF's "slightly under 80%" (S32, S33). The fact sheet compares IEHP only with Molina, and the CHCF data are from Dec 2024. Even against Molina alone, IEHP is about 88% [ESTIMATE: arithmetic]. Cite CHCF |
| CHCF date | "June 2026" is the slide deck (S33). The full report's cover says April 2026 and the file is dated Sept 2026 (S32). Its web page slug says 2025 |
| Group table "Lose this doctor unless..." | Oversimplifies; see section 3 |
| HPSA scores (Ref 5, 3RNET); Source F date | **Not checked** in this workstream |

---

## 10. Competition materials

**Confidence: High for the CPP page. Medium that nothing else exists publicly, since a private course site would not be visible.**

| Item | Result |
|---|---|
| **CEO Business Challenge page** | **Found** (S43). 2026 challenge "Analyzing Health-Care Service Models for Inland Empire Health Plan (IEHP)," presented by IEHP's CEO |
| **Dates** | Registration Sep 21 to Oct 16 (closed). **Final presentations, awards and networking: Thursday, November 19, 2026, 1:00 to 3:30 PM** |
| **Team and prizes** | Teams of 3 to 5, CPP students. Cash prizes for top three. Digital badges |
| **Scoring** | Teams "present actionable insights and solutions to a panel of industry and academic leaders" |
| **Public rubric or rules** | **Not found** |
| **IEHP Case Document** | **Not found publicly.** The guide requires it, and the page's "A Message from the IEHP CEO" section has no text in the page source, possibly a video |
| **Financial Impacts Modeling Spreadsheet** | **Not found publicly** |
| Contacts | Listed on the page (Dr. Rita Kumar; Singelyn Center). Not contacted |

The project cannot confirm what the case asks for. **The owner should supply these documents if they hold them.** Anything here that assumes the case's scope is provisional.

---

## What this changes for the analysis

### Corrections to the guide's framing
1. **Drop "the IEHP number is not public."** Anchor on IEHP's published 100,000+ and about 10%. The 14% and 18% scenarios should be presented, at most, as comparisons that exceed IEHP's own statement. Ask IEHP which it means and whether it includes QNC members.
2. **Change the provider framework.** The guide's four groups miss the largest risk. Split Group A into *active FFS billers* and *enrolled but dormant*. Add *ORP-only* and *different NPI* as checks. Statewide, dormant providers outnumber non-enrolled ones about 2.25 to 1 (S35). **A recommendation focused only on getting Group B enrolled would miss most of the problem and is constrained by processing time.**
3. **"Enroll in time" is not a simple deadline.** Do not say providers will lose their patients on a clean date until DHCS resolves "approved" vs "submitted."
4. **The guide's ZIP ratio measures general FFS supply against all Medi-Cal members.** It does not measure the access gap for people moving. Source A counts all eligibles across plans and FFS, and movers' locations are unknown and must stay unmapped under the contract. Label it as such. Do not rank ZIPs as "where transitioning members lose access."

### Timing
5. **Sort every recommendation by date.** With 17 days to the final and 60 to the transition, separate what can be done before January 1 from what must work afterward. Dates that fall before or around the presentation include Nov 6, Nov 15 and Dec 1.
6. **Model two cliffs.** January 1 is about delivery system and coordination. July 1, 2027 adds clinic payment cuts, dental cuts, premiums and loss of scope for some. FQHCs look like the natural anchor for January, yet their finances worsen in July. A plan built on FQHC capacity must say what happens then.
7. **The moving population shrinks over time.** Use date-stamped denominators.

### Candidate interventions

| Intervention | Possible? | Key constraint |
|---|---|---|
| Reactivate dormant FFS-enrolled network providers | **Yes, likely highest yield** | Accepting patients is voluntary; rate gap |
| PAVE concierge for non-enrolled network providers | **Yes, before Jan 1** | 90 or 180 day window; individual signature |
| TAR pre-submission and special handling | **Yes,** open since Nov 1 | Provider must be FFS-enrolled |
| High urgency handoffs | **Required already** | Must be counted as baseline, not new value |
| 90-day prescriptions and refills | **Yes,** IEHP is doing it | Prescriber enforcement pending |
| CHW navigation billed to FFS | **Conditional** | Enrolled supervising provider; non-tribal FQHC and RHC CHWs not billable; DHCS says codes do not guarantee payment |
| Continue ECM or Community Supports as Medi-Cal benefits | **No** | Not covered in FFS |
| IEHP-funded care management for former members | **Open** | Funding authority unresolved; Community Reinvestment is the lead to test |
| Continuity-of-care rights for 12 months | **No** | Statute expressly does not apply |
| IEHP paying claims or top-ups after Jan 1 | **Open, risky** | Cross-subsidy concern in S16; public-plan limits unexamined |
| Partner with DHCS's vendor or navigators | **Conditional** | Vendor unnamed; grants may be set |
| Transport fixes | **Needs U01** | The 86% broker claim decides the size of this problem |
| Behavioral health focus | **Target non-specialty** | That is the part moving to FFS; county specialty care is unchanged |
| Dental | **Not IEHP's lever** | Already FFS; change comes July 2027 |
| Member-level lists or maps of UIS members | **No** | Contract; PHI; enforcement climate |

### Finance
8. **Treat capitation loss as gross revenue, not as the financial impact.** Use the bounds as ranges and state that UIS risk corridors already limit margin. The Financial Impacts spreadsheet may give different inputs.
9. **Use California's fee values, not only the national ones,** and cite 0.56 alongside 87.5% with their definitions. **Treat any IEHP-to-FFS rate gap as an assumption.**

### Open questions for the gate
- **For DHCS Provider Enrollment:** must a provider be approved, or only have applied, by January 1? Will services after the application date be paid once approved?
- **For IEHP:** is it 100,000 or 132,000+? Does it include QNC? Is there a county split that may be shared under the contract?
- **For the owner:** do you hold the Case Document, spreadsheet and rubric? Keep the guide's 10/14/18% scenarios for comparison, or replace them? May CHCF tracker county data be consulted, given that it may derive from the prohibited aid-category file?
- **For a person with a browser:** open U01, U02 and U03 (DHCS decks) and U07 (APL 25-004 and Appendix A). These could change the transport, enrollment and Community Reinvestment findings. Re-check archived pages against live versions before quoting them.

### Could not be established
- County-level or Molina and Kaiser UIS counts for Riverside and San Bernardino.
- IEHP's capitation dollars for this group, and its contract rates.
- Actual current PAVE processing times, or any expedited route.
- Whether "approved" or "submitted" controls on January 1.
- Whether non-members can benefit from Community Reinvestment or other plan funds.
- Final clinic policy letter text, including FFS PPS claim mechanics and Tribal treatment.
- Whether the CMS Medicare rule was finalized.
- The reason KFF's primary care index differs from the 87.5% target.
- The competition's rubric and case documents.
