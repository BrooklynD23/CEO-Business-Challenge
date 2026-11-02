# Analysis findings (Phase 1): FFS supply, scenarios, correlations and a preliminary gap ranking

Analysis workstream, 2026-11-02. Labels: `[COMPUTED: script]`, `[VERIFIED: source]` (from `research/policy_verification.md` or a file I read), `[ESTIMATE: ...]`, `[UNVERIFIED]`.

## How to read this file

- **Framing rule.** The ZIP/ZCTA ratio and every ranking here measure *general FFS supply against all Medi-Cal eligibles (managed care and FFS together)*. They do not show where transitioning members will lose access. Rankings are titled "general FFS supply shortfall among all Medi-Cal eligibles".
- **Denominators, never mixed.** Raw ratios and catchments: all Medi-Cal certified eligibles, source A, 2026-09 (preliminary). Scenarios: IEHP movers, all-plan movers, existing FFS members (source B, 2026-09, preliminary). Numerators: FFS-enrolled provider records or unique NPI-ZIP pairs in source E (as of 2026-10-26), not people accepting patients.
- **Sensitive limit.** Movers are county or regional totals. "Does the uniform assumption matter?" is answered with status-blind random Dirichlet and random-field draws that use no covariate. LEP (ACS C16001) is an access-need correlate only. Race/ethnicity is county-level in B and unused here.
- **Statistics.** Spearman with 2,000-draw bootstrap CI. Benjamini-Hochberg (BH) over all 69 correlation tests, and separately within model terms and Moran tests. Eligibles-weighted rho, jackknife range and 5%-trimmed rho for outliers. Negative-binomial counts with a log-eligibles offset. Cluster-robust SEs by ZIP3 (only 7 clusters) and HC. Moran's I and LISA with 999 permutations on queen contiguity. Correlation, not cause. Non-significant is not "no effect".
- **Analysis sample.** 130 ZCTAs: assigned to Riverside or San Bernardino, at least 500 eligibles in 2026-09, not suppressed, with a polygon. Rates use Poisson-gamma empirical-Bayes shrinkage (prior CV about 1.8).

## 0. Ranked findings

| # | Finding | Headline | Confidence |
|---|---|---|---|
| 1 | The FFS population multiplies about 2 to 3.5 times, and IEHP-only framing understates it by 14% to 57% | Mid 132,000 on 99,206 existing FFS = 2.33x (2.17x lag-adjusted) | Medium |
| 2 | On paper the extra load per PC record is small, so limits are acceptance, dormancy, place and concentration | Mid: 32 to 53 extra patients per accepting PC record (b); 49 to 80 with 34% dormant | Low to medium |
| 3 | Source E is nearly the whole physician workforce, so "FFS-enrolled" is not selective | E physician NPIs = 99% of CHCF all-payer (IE); PC physicians = 125% | High (comparison) |
| 4 | The guide's raw ratio misleads: 43% of PC records sit at 100+-NPI addresses; neighbours ignored | Raw vs catchment rho 0.34 (0.18 to 0.48) | High |
| 5 | A preliminary shortfall ranking is stable to weights, demand unevenness and dormancy, less so to supply definition; report tiers | 6 Tier 1, 4 Tier 2, 6 Tier 3 ZCTAs | Medium |
| 6 | Rurality is the dominant divide (rho -0.58 with RUCA); poverty is unrelated to PC supply but related to MH and dental | Non-metro PC catchment 1.26 vs 3.31 | High (association) |
| 7 | The self-reported new-patient flag says 87% accept FFS, from a selected 4.4% of rows | Audit range 40-65% | High (number), low (meaning) |
| 8 | Classification limits "primary care by ZIP"; Provider_Source 3 looks ORP-type | 68% of IE rows have no specialty; PC 9,778 (a) to 3,974 (e) | High |
| 9 | HPSA overlaps FFS access gaps but misses a third of the lowest-access ZCTAs | Sensitivity 70%, kappa 0.43 | Medium |
| 10 | Existing FFS counts for recent months are revised upward; 2026-09 is about 12% low | 99,206 vs 112,539 | Medium |

## 1. How large FFS becomes, and what IEHP-only framing leaves out

**Question and method.** How many members move, how much does FFS grow in the two counties, and what do Molina, Kaiser and other plans add? Arithmetic on IEHP Medi-Cal 1,321,983 (fact sheet), B 2026-09 delivery system by plan, and the scenarios in `policy_verification.md` (IEHP Governing Board 2026-08-10: "more than 100,000 ... about 10%") [VERIFIED: S22]. Existing FFS = Riverside 52,453 + San Bernardino 46,753 = 99,206 (preliminary). Lag-adjusted base = mean of 2026-06 to 08 = 112,539 [ESTIMATE].

Non-IEHP exposed members in B 2026-09 are 374,181:
- Kaiser 189,300
- Molina 151,975
- Out-of-county plan 24,338
- SCAN 8,568

PACE (3,399) is excluded because PACE members stay in PACE. IEHP is 78.0% of managed care in the two counties (1,340,442 of 1,718,022). Kaiser is 11.0% and Molina 8.8%, the reverse of the Dec-2024 CHCF split.

Non-IEHP mover rate = IEHP's rate x 0.5, 1.0 or 2.0. The statewide pattern (IEHP 10.0% of plan enrolment, 5-7% of movers) implies roughly 1.5 to 2.1x [ESTIMATE: arithmetic on S35/S32]. That is a statewide ratio, not an IE fact.

| Scenario | IEHP movers | Share of 1,321,983 | FFS multiple (99,206 base / 112,539 lag-adj.) | All-plan movers, other plans at 0.5x / 1x / 2x | Extra pts per accepting PC record (b), 65% to 40% acceptance | same, 34% dormant |
|---|---|---|---|---|---|---|
| Low (IEHP ">100,000") | 100,000 | 7.6% | 2.01x / 1.89x | 114,152 / 128,305 / 156,609 | 25-40 | 38-61 |
| Mid (IEHP "about 10%") | 132,000 | 10.0% | 2.33x / 2.17x | 150,681 / 169,362 / 206,724 | 32-53 | 49-80 |
| High (+~15k QNC, may double count) | 155,000 | 11.7% | 2.56x / 2.38x | 176,936 / 198,872 / 242,744 | 38-62 | 58-94 |
| Guide 10% | 132,198 | 10.0% | 2.33x / 2.17x | 150,907 / 169,616 / 207,034 | 32-53 | 49-80 |
| Guide 14.0% | 185,078 | 14.0% | 2.87x / 2.64x | 211,271 / 237,463 / 289,849 | 45-74 | 69-113 |
| Guide 1-in-7 | 188,855 | 14.3% | 2.90x / 2.68x | 215,582 / 242,310 / 295,764 | 46-75 | 71-115 |
| Guide 18% | 237,957 | 18.0% | 3.40x / 3.11x | 271,633 / 305,310 / 372,662 | 58-95 | 89-145 |

The guide rows exceed IEHP's own figure and are comparison only.

**Guide rounding.** "About 190,000 at about 14%" is 14.37%. 14.0% gives 185,078 and 1/7 gives 188,855. The guide's middle row is overstated by 1,100 to 4,900. Its 132,000 and 238,000 rows are fine.

**Effect.** At IEHP's mid figure, movers are 1.33x existing FFS (FFS 2.33x). All-plan adds 28% at IEHP's rate, 14% at half, 57% at double. All-plan FFS multiples are 2.2x to 3.5x on the published base. DHCS's statewide figure is 3.85x [VERIFIED: S01].

**Existing FFS and vintage.**
- 2026-09 is 99,206, against 111,790 in August and a Jun-Aug mean of 112,539. September is 11.8% below the mean. October (66,869) is 40.6% below.
- DHCS quotes April 2026 FFS as 702,547 [VERIFIED: S01]. The 2026-10-07 snapshot has 745,220 (+6.1%). Managed care moved +0.16%. That is what upward revision as months mature looks like; the DHCS quote's vintage date is not stated.
- **Older vintages could not be compared.** Only the 2026-10-07 snapshot was obtained, and the Internet Archive was offline on 2026-11-02.
- Eligibles in the two counties fell 8.0% from 2025-09 (1,974,108, final) to 2026-09 (1,817,228). Managed care fell 7.7%; mature FFS was flat (113,401 vs about 112,500). Use date-stamped denominators.

**Age.** No age restriction. Applying statewide shares only (251,000 of 1.9 million under 21; 28.8% age 50+ of the expansion group) gives roughly 13,000 to 20,500 under 21 and 29,000 to 45,000 aged 50+ for IEHP's primary range [ESTIMATE].

**Limits.** IEHP's figure may or may not include QNC. Other plans' rates and Kaiser/SCAN exposure are unknown. The IEHP county split (about 50/50 by membership) is uniform. The lag base is borrowed. Sources: `policy_verification.md` (S22, S35, S31, S32, S01), B table 2, C fact sheet. [COMPUTED: s04_scenarios.py]

## 2. Extra patients per provider; required acceptance

**Question.** How many extra patients per accepting PC provider, and what acceptance or added panel would be needed?

**Variables.** IE PC records (physicians with PC specialty plus NPs) from E:
- a broad 9,778
- b deduped NPI-ZIP 6,261
- c strict 6,254
- d billable-at-site 5,086
- e address-capped 3,974

Acceptance 40-65% [ESTIMATE: `intervention_evidence.md` 2.2; no FFS-list audit exists]. Dormancy 0% and 34.4% (45,000 of about 131,000 enrolled plan-serving providers statewide, per CMA's report of DHCS's 9/30 webinar) [ESTIMATE: borrows a statewide ratio from a different population; not an IE measurement].

**Formula.** Extra per accepting provider = movers / (records x (1 - dormancy) x acceptance).

**Effect, mid 132,000, definition b.**
- Spread over every record: 21 extra patients (existing FFS load is 15.8 members per PC record, 18.0 lag-adjusted).
- Accepting only: 32 (65% accept) to 53 (40%). With 34% dormancy, 49 to 80.
- Physicians only (5,084): 40 to 65, or 61 to 99 with dormancy.
- Address-capped (3,974): 51 to 83, or 78 to 127.
- Broad (9,778): 21 to 34.
- If a quarter of records carried everything (Ludomirsky: 25% of PCPs deliver 86% of Medicaid primary care), 84 each.

**Required acceptance (b, mid).**
- 42% to keep the load at 50 patients per accepting record; 21% at 100.
- For the address-capped count: 66% and 33%, so at the top of the audit range the mid scenario already exceeds 50 per accepting record.
- At 40% acceptance the 53-patient added panel is 3.8% of a 1,387 panel, 2.7% of 1,947 and 2.3% of 2,300 [ESTIMATE; panel figures are UNVERIFIED search summaries in `intervention_evidence.md` 2.4; no Medicaid-specific cap exists].

**Meaning.** On a headcount basis the arithmetic is not tight, but that is about records, not capacity (finding 3). Binding questions are acceptance, dormancy, geography and concentration. **Limits.** All movers are treated as PC patients; no specialist, behavioural or dental demand is added. Tables: `s04_extra_patients_per_ffs_provider.csv`, `s04_required_acceptance_or_added_panel.csv`, `s04_added_panel_vs_benchmark.csv`. [COMPUTED: s04_scenarios.py]

## 3. "FFS-enrolled" is nearly the whole physician workforce (sanity check)

**Question.** Does E's physician count look like a subset of IE physicians? CHCF (2024, all payers) reports per 100,000 [VERIFIED: S32]:

| Measure | IE | CA |
|---|---|---|
| Physicians | 229 | 358 |
| Primary care | 85 | 118 |
| Specialty | 115 | 176 |
| Psychiatry | 11 | 18 |

IE population 4,769,007 (guide), so 85 per 100,000 is about 4,054 PCPs.

| Unique physician NPIs per 100,000 | E, IE | CHCF, IE | E/CHCF | E, CA | CHCF CA | E/CHCF |
|---|---|---|---|---|---|---|
| Physicians, all sources | 241.5 | 229 | 105% | 350.3 | 358 | 98% |
| Physicians, Source 1-2 | 227.6 | 229 | 99% | 318.6 | 358 | 89% |
| Primary care physicians | 106.3 | 85 | 125% | 136.5 | 118 | 116% |
| Specialists (non-PC, non-psychiatry) | 113.1 | 115 | 98% | 173.9 | 176 | 99% |
| Psychiatrists | 8.9 | 11 | 81% | 12.6 | 18 | 70% |

In the IE, 5,069 unique PC-physician NPIs (vs about 4,054 implied) plus 1,655 NPs.

**Meaning.** Nearly every physician is enrolled, so enrolment does not separate people who see Medi-Cal FFS patients from those who do not. The PC count exceeds an all-payer benchmark, so it includes people not practising primary care in the IE (hospital-based internists coded general internal medicine, part-time or out-of-area physicians, a different CHCF definition and year). No per-100,000 ratio from E should be read as capacity. **Limits.** CHCF counts active physicians in 2024 with its own definition; I cannot decompose the 25% overshoot.

**IEHP network comparison.** IEHP lists PCP 1,488, specialists 2,817, behavioural health 3,453, hospitals 34, other 2,570 (10,362, mixing individuals and facilities) [VERIFIED: C]. E's 6,261 PC NPI-ZIP pairs are a different population (every FFS-enrolled record vs plan-contracted assignments), unit and date. No defensible comparison exists without IEHP's NPI-level directory, which was not downloaded; that file is what splits Groups A, B and C. "PCP - FFS" in IEHP board material describes how IEHP pays a PCP and was not treated as Medi-Cal FFS enrolment.

**Dormancy what-if.** E has no claims, so dormancy cannot be seen. Random dormancy of 20/34/50% leaves ranks essentially unchanged (rho 0.998-0.999, top decile retained 91-92%) but raises the load per active record 1.25x to 1.8x. It cannot be applied by ZCTA. [COMPUTED: s02b_supply_diagnostics.py, s06_ranking.py]

## 4. Why the raw ZIP ratio misleads, and what the catchment changes

**Method.**
- Raw ratio: PC records (b) per 1,000 all Medi-Cal eligibles (A, 2026-09).
- Catchment: enhanced two-step floating catchment area with Gaussian decay (Dai 2010).
- Distance: straight-line between population-weighted ZCTA points (tract centres of population weighted by tract-ZCTA overlap) and provider coordinates. **It is a proxy, not travel time.**
- Radii: 15, 30, 50 km fixed, and a RUCA-variable 15/30/60 km.
- Coverage: all California ZCTAs and providers within 150 km of an IE ZCTA, so Los Angeles, Orange, San Diego, Imperial, Kern, Inyo and Ventura are included. n = 130 ranked ZCTAs (744 demand points, 18,282 supply locations).

**Raw vs catchment, Spearman (95% CI), definition b:**

| Group | 15 km | 30 km | 50 km | RUCA-variable |
|---|---|---|---|---|
| Primary care | 0.53 (0.38 to 0.66) | 0.34 (0.18 to 0.48) | 0.28 (0.11 to 0.44) | 0.41 (0.24 to 0.56) |
| Mental health | 0.70 (0.59 to 0.78) | 0.54 (0.41 to 0.66) | 0.40 (0.23 to 0.53) | 0.59 (0.45 to 0.71) |
| All specialists | 0.55 (0.42 to 0.67) | 0.33 (0.18 to 0.48) | 0.22 (0.06 to 0.39) | 0.40 (0.25 to 0.55) |
| Dental | 0.73 (0.63 to 0.81) | 0.59 (0.45 to 0.70) | 0.53 (0.39 to 0.65) | 0.55 (0.39 to 0.68) |

For PC at 30 km the lowest-quintile overlap is 42% and the median ZCTA moves 30 ranks. With the RUCA-variable catchment:
- 10 ZCTAs in the raw ratio's worst quintile are ordinary or good by catchment (false alarms). Examples: 91784, 92285, 92276, 92368, 92359, 92313, 92282, 92397, 92549, 92391.
- 7 ZCTAs the raw ratio calls average or good fall in the catchment's worst quintile ("hidden"): 91708, 92539, 92342, 92530, 92883, 92585, 92586. 92530 has 27,992 eligibles.
- 10 are low on both.

**Hospital-campus concentration is the main distortion.**
- 71% of IE street addresses carry one NPI, but 28 carry 100 or more (58 carry 50 or more; the largest 1,626).
- 23.6% of all IE rows and **43% of PC records (b)** are at addresses with 100 or more NPIs (23% at 500 or more).
- Capping each address at 25 PC records cuts the PC count by 37% (6,261 to 3,974).
- Seven of 164 ZCTAs hold half of all PC records (14 after the cap). The 10 largest hold 59%.
- 57 of 164 IE-assigned ZCTAs (35%; 109,759 eligibles, 6.1%) have no PC record.
- Loma Linda's ZCTA (92354) has 128 records per 1,000 eligibles raw and 5.9 by catchment, against a 3.45 regional average.
- Campus share correlates +0.53 with the raw ratio (CI 0.41 to 0.64, BH p < 0.001) and +0.34 with the catchment.

| Gini and concentration (164 IE ZCTAs) | Total | Gini | ZCTAs holding half | ZCTAs with none |
|---|---|---|---|---|
| PC (MD+NP) | 6,262 | 0.83 | 7 | 35% |
| PC physicians | 5,086 | 0.84 | 6 | 38% |
| Mental health | 4,661 | 0.83 | 8 | 37% |
| Specialists | 5,956 | 0.86 | 6 | 40% |
| Cardiology | 275 | 0.89 | 6 | 74% |
| Endocrinology | 43 | 0.90 | 6 | 85% |
| Dental | 4,628 | 0.70 | 19 | 38% |
| Clinics | 222 | 0.67 | 22 | 50% |
| Eligibles | 1,813,508 | 0.55 | 30 | n/a |

**Border effect.** Dropping neighbouring counties lowers PC catchment by a median 14% (-23% to -1%) in the 7 ZCTAs within 12 km of a non-IE ZCTA point, and by 0% for interior ZCTAs. Out-of-state border providers (NV, AZ) were *not* added to the primary measure. Their local non-Medi-Cal populations are not in the denominator, so adding them gives absurd values for the Colorado River ZCTAs (53 per 1,000 for 92363 vs 1.5 without) and changes nothing elsewhere. The data allow out-of-state supply but not demand. The IE-only analysis correlates 0.99 with the primary spec.

**Urban vs desert.** Median PC catchment by class, 15 / 30 / 50 km:
- Riverside metro (63 ZCTAs): 1.8 / 2.4 / 2.9
- San Bernardino metro (47): 2.8 / 3.7 / 4.2
- San Bernardino small town (11): 1.3 / 1.2 / 1.1
- San Bernardino rural (7): 0.3 / 1.3 / 1.5

Raw ratio medians are 0.65, 0.84, 0.33 and 0.00. The same records mean different things at different radii. Chino-area 91710 has raw 2.9 and catchment 2.0 / 3.7 / 4.6. Twentynine Palms 92277 has raw 0.34 and catchment 0.34 / 0.55 / 0.44. Needles 92363 stays at 1.5 at every radius. Catchment rank agreement across radii is modest (30 vs 50 km 0.84; 15 vs 50 km 0.61), so the radius is a real choice.

**Diagnostics and limits.**
- Catchments are smooth by construction (Moran's I 0.83) while the raw ratio is nearly random (I 0.05, p 0.086).
- 88 IE rows had geocodes more than 40 km from their ZIP and fell back to the ZCTA point.
- The catchment treats all Medi-Cal eligibles as competing for FFS records. A scenario-demand variant (existing FFS plus 1/7 of managed care) correlates 0.9997 with the primary.

Sources: E, A, ACS 2020-2024, Census 2020 relationship and tract populations. [COMPUTED: s03_access.py, s02b_supply_diagnostics.py, s05b_correlations.py]

## 5. Preliminary "general FFS supply shortfall" ranking and stability

**Components** (percentile shortfall, higher = worse), n = 130:
- PC, mental-health, specialist and dental catchments from the RUCA-variable catchment. Demand = existing FFS plus 10% of managed care, uniform within county.
- An access-need component: chronic need, no vehicle and poverty. LEP excluded.

**Weights.**
- Equal: 0.2 each.
- Evidence-informed [ESTIMATE: judgement]: PCP 0.35, MH 0.20, specialist 0.15, dental 0.05, need 0.25.
- PCA: first component explains 66%; weights 0.24, 0.24, 0.22, 0.21, 0.09.
- A 2,000-draw uniform Dirichlet weight sweep.

**Demand stress tests (all status-blind).**
- Dirichlet draws of ZCTA shares of county mover totals (150 draws at each of six dispersions).
- Smoothed log-normal random fields (100 draws each).
- Random provider dormancy (100 draws).

**Effect.**
- Equal vs evidence weights rho 0.99 (top-decile overlap 85%); equal vs PCA 0.99 (85%); evidence vs PCA 0.97.
- The guide's raw ratio rank agrees with the composite at rho 0.40 and shares only 15% of the top decile.
- 16 ZCTAs reach a tier. Tier 1-2 hold 71,874 eligibles (4.0% of ranked); with Tier 3, 138,422 (7.7%).

| ZCTA | County | Eligibles | Rank 5th-95th pct | Top-decile freq: weights / weights+demand (min) | Guide raw rank | Tier |
|---|---|---|---|---|---|---|
| 92254 | Riverside | 9,672 | 1-4 | 100 / 100 | 18 | 1 |
| 92256 | San Bernardino | 1,438 | 1-4 | 100 / 100 | 26 | 1 |
| 92274 | Riverside | 12,624 | 2-12 | 97 / 97 | 2 | 1 |
| 92230 | Riverside | 1,562 | 3-15 | 93 / 93 | 23 | 1 |
| 92365 | San Bernardino | 1,168 | 4-11 | 98 / 98 | 30 | 1 |
| 92372 | San Bernardino | 2,594 | 3-20 | 82 / 82 | 15 | 1 |
| 92539 | Riverside | 2,295 | 5-19 | 80 / 78 | 58 | 2 |
| 92536 | Riverside | 1,194 | 2-23 | 75 / 75 | 28 | 2 |
| 92570 | Riverside | 34,325 | 6-21 | 68 / 68 | 46 | 2 |
| 92567 | Riverside | 5,002 | 9-20 | 68 / 68 | 5 | 2 |
| 92363 | San Bernardino | 2,690 | 3-30 | 56 / 27 | 82 | 3 |
| 92371 | San Bernardino | 8,097 | 7-34 | 52 / 44 | 35 | 3 |
| 92240 | Riverside | 24,138 | 6-30 | 49 / 49 | 1 | 3 |
| 92225 | Riverside | 7,125 | 4-32 | 47 / 42 | 80 | 3 |
| 92356 | San Bernardino | 3,909 | 3-40 | 45 / 21 | 39 | 3 |
| 92311 | San Bernardino | 20,589 | 7-27 | 31 / 25 | 81 | 3 |

Tier 1 = top decile in at least 80% of draws; Tier 2 = 50-79%; Tier 3 = 20-49%. For 20 of 130 ZCTAs the 5th-95th percentile rank range exceeds 50 places, so quote tiers or ranges, never single ranks. Nearly all Tier 1-3 ZCTAs are small desert, mountain or foothill ZCTAs (RUCA 2-10; RUCA is commuting-based and rates the Coachella-valley ones 2-3). Larger exceptions are 92570 and 92240. By exposure (shortfall x eligibles) the top ZCTAs are different and larger (92345, 92570, 92530, 92553, 92392; intensity-exposure rho 0.31); both lists are in `s06_gap_ranking_zcta.csv`.

**Does the uniform-share assumption matter?** Not much for this ranking.

| Dirichlet alpha | Realised CV of ZCTA share | ZCTA mean rho | ZCTA 5th pct | 4-digit prefix | ZIP3 | Baseline top decile retained |
|---|---|---|---|---|---|---|
| 10,000 | 0.61 | 0.999 | 0.999 | 0.999 | 0.985 | 93% |
| 1,000 | 1.64 | 0.997 | 0.995 | 0.993 | 0.978 | 90% |
| 300 | 2.23 | 0.992 | 0.987 | 0.984 | 0.975 | 87% |
| 100 | 2.97 | 0.982 | 0.968 | 0.971 | 0.961 | 83% |
| 30 | 4.64 | 0.955 | 0.930 | 0.936 | 0.909 | 79% |

Coherent random fields (10 and 25 km) at CV up to 1.1: mean rho 0.93 to 0.99, top decile retained 80% to 90%. That is a statement about status-blind randomness only. What does move the ranking is the weights (mean rho 0.95 over the sweep, 5th percentile 0.86) and the supply definition (top-decile overlap between definitions a, b, c, e: 69% to 85%; rho 0.97 to 0.996).

**Unit.** Weight-sweep stability is the same at ZCTA level (0.950) as for 39 four-digit ZIP prefixes (0.951) and lower for 7 ZIP3 units (0.921). Only four county-by-RUCA units are stable (0.998), but they say little. Recommendation: rank ZCTAs and report tiers; use 4-digit prefixes only for communication. Aggregating buys no stability.

**Limits.**
- Built on enrolment counts (finding 3).
- Small ZCTAs rank high partly because tiny demand makes ratios sensitive.
- 28 ZCTAs under 500 eligibles, 5 without polygons and 6 suppressed or absent are unranked.
- Dental uses stale (Oct 2025) billing addresses.

[COMPUTED: s06_ranking.py]

## 6. Urban west vs desert east; steepest category gap

**Method.** Cliff's delta (non-metro RUCA 4+ n = 20 vs metro n = 110, bootstrap CI). Eligibles-weighted IE vs neighbouring-county accessible supply at 30 km, definition b. CHCF all-payer IE/CA ratios (physicians 64%, PC 72%, specialty 65%, psychiatry 64%) are the outside reference.

**Effect.**
- Non-metro PC catchment is lower: delta -0.71 (95% CI -0.84 to -0.54, BH p < 0.001; medians 1.26 vs 3.31). MH delta -0.86 (-0.94 to -0.77).
- In the raw EB ratio the difference is only -0.09 (-0.32 to 0.14; adj p 0.58), so **the raw ratio hides the desert gap**.
- Within San Bernardino: -0.85 (-0.96 to -0.69, n = 65).
- The two counties do not differ (delta +0.01, adj p 0.91).

IE vs neighbours (1.00 = parity):

| Category | IE / neighbours | IE / LA+OC+SD |
|---|---|---|
| Endocrinology (43 records) | 0.39 | 0.33 |
| Cardiology | 0.62 | 0.54 |
| All specialists | 0.65 | 0.57 |
| Clinics | 0.67 | 0.60 |
| OB/GYN | 0.72 | 0.63 |
| PC physicians | 0.78 | 0.68 |
| Psychiatrists | 0.80 | 0.69 |
| Primary care (MD+NP) | 0.82 | 0.72 |
| Dental (F) | 0.93 | 0.81 |
| Nurse practitioners | 1.07 | 0.94 |
| Mental health | 1.31 | 1.14 |

**Meaning.** Specialist categories show the steepest gap. Mental health is not short in enrolled counts, but those are mostly therapists whose FFS acceptance cannot be seen. The ordering (specialty about 0.65, PC about 0.8) echoes CHCF's all-payer ratios (0.65, 0.72). Endocrinology is unstable (43 records). **Limits.** Inherits the E-vs-capacity problem; only 20 non-metro ranked ZCTAs. [COMPUTED: s05b_correlations.py]

## 7. The `Medicaid_Patients` flag

**Variables and n.** 1,614 of 36,470 IE rows (4.4%) carry the flag. All are FFS billing rows from Provider_Source 1: 15.4% of 10,497 billing rows and none of the 25,973 non-billing rows.

| Value | Meaning | Rows | Share |
|---|---|---|---|
| B | both FFS and managed care | 1,283 | 79.5% |
| F | FFS only | 118 | 7.3% |
| M | managed care only | 76 | 4.7% |
| N | no new Medicaid | 137 | 8.5% |

**Effect.**
- B or F (will take new FFS patients) = 1,401 of 1,614 = **86.8%** (95% CI 85.1% to 88.4%), 22 to 47 points above the 40-65% audit range.
- Riverside 85.6%, San Bernardino 88.6%.
- PC physician and NP flagged rows (273): 90.5% (240 B, 7 F, 14 N, 12 M).
- M plus N (declining new FFS) = 13.2%.

**Selection.**
- Flagged rows are organisations more often (87.0% type 2 vs 78.6% of unflagged billing rows).
- 54% report telehealth vs 0.8% of unflagged billing rows.
- Logistic model of carrying the flag among billing rows (HC1, n = 10,497):

| Predictor | OR (95% CI) | p |
|---|---|---|
| Clinic | 2.51 (1.94 to 3.25) | < 0.001 |
| Physician | 0.51 (0.41 to 0.63) | < 0.001 |
| Mental-health individual | 0.31 (0.23 to 0.42) | < 0.001 |
| Organisation (type 2) | 1.21 (1.01 to 1.44) | 0.035 |
| log NPIs at address | 1.08 (1.04 to 1.13) | < 0.001 |
| San Bernardino | 0.94 (0.84 to 1.05) | 0.26 |

**"M".** M providers are FFS-enrolled (they are in E) but say they take managed-care Medicaid patients only: a partial self-reported view of Group A providers who would not take moving members. It is a floor (76 rows; the flag is absent from 95.6% of rows). **Limits.** Self-report, undated and unverified. Stated willingness is not a bookable appointment. Do not use 86.8% as an acceptance rate. [COMPUTED: s04_scenarios.py]

## 8. Supply definitions, classification, and Provider_Source 3

Definitions:
- (a) broad: every enrolled record that fits, no dedupe, groups included, plus unknown-specialty physicians for PC.
- (b) deduped NPI-ZIP, individuals, Source 1 or 2, group entities removed.
- (c) strict: b, Source 1 only, hospital-based specialties removed (radiology, anesthesiology, pathology, emergency/urgent care, nuclear medicine, radiation therapy, hospitalists), and flag N or M removed.
- (d) billable at site: c restricted to own-NPI billers or records sharing an address with a billing record.
- (e) b with each street address capped at 25 records per group.

Dental is from F (Oct 2025, 13 months old, billing addresses).

| Group | a | b | c | d | e |
|---|---|---|---|---|---|
| PC physicians | 7,686 | 5,084 | 5,077 | 4,010 | 3,177 |
| Nurse practitioners | 2,092 | 1,177 | 1,177 | 1,076 | 1,049 |
| PC (MD+NP) | 9,778 | 6,261 | 6,254 | 5,086 | 3,974 |
| FQHC/RHC (035) | 168 | 144 | 143 | 143 | 144 |
| All clinics | 274 | 223 | 220 | 220 | 223 |
| Mental health | 6,990 | 4,655 | 4,648 | 4,177 | 3,306 |
| Psychiatrists | 523 | 426 | 425 | 367 | 351 |
| Cardiology | 343 | 276 | 275 | 211 | 276 |
| OB/GYN | 778 | 604 | 604 | 432 | 517 |
| Endocrinology | 50 | 43 | 43 | 40 | 43 |
| All specialists | 7,306 | 5,952 | 3,289 | 2,569 | 3,683 |
| Dental (F) | 7,414 | 4,714 | 4,535 | 4,529 | 4,714 |

PC records fall 2.5-fold from a to e. Strict halves specialists (7,306 to 3,289).

**Ranking effect** (Spearman across 130 ZCTAs; lowest-quintile overlap in brackets):

| Group | a vs b | a vs c | b vs d | b vs e |
|---|---|---|---|---|
| PC | 0.93 (73%) | 0.93 (73%) | 0.97 (85%) | 0.99 (100%) |
| Mental health | 0.93 (69%) | 0.93 (69%) | 0.99 (96%) | 0.99 (100%) |
| All specialists | 0.96 (85%) | 0.88 (65%) | 0.85 (69%) | 1.00 (100%) |
| Dental | 0.98 (89%) | 0.97 (73%) | 0.99 (85%) | 1.00 (100%) |

Rankings are robust for PC and mental health, and less so for specialists under strict or billable definitions (0.83 to 0.91).

**Classification coverage.**
- 68.2% of IE rows have no specialty (statewide 64.2%; CHCF 63.7%).
- 13.0% have unknown type (statewide 11.1%; CHCF 11.1%).
- Of 12,833 physician rows, 23.2% have no specialty code. NUCC taxonomy rescued 1,594; 11.1% stay unclassifiable.
- Of candidate PC rows (PC specialty, unknown-specialty physician, NP), 17.4% have unknown specialty. The guide's "primary care by ZIP" is reliable for about five in six candidate rows.
- 4,754 IE rows (13%) are Source 2 or 3 records with no type.

**Record counts vs CHCF.** County-label counts match CHCF's 2026-09-25 figures within 1% (Riverside 13,402 vs 13,267; San Bernardino 14,890 vs 14,781). Statewide is 380,888 vs 373,367 (+2.0%, later file). The 36,470 IE rows are higher because 8,428 rows (23%) carry County = N/A and are recoverable only through lat/lon CountyName. Rows 36,470 and NPIs 30,520 match the data report.

**Provider_Source 3 (ORP-type).**
- All 68,279 statewide Source 3 rows are Type 1 individuals and 100% non-billing. None carries the flag or a taxonomy.
- Only 15.9% of their NPIs appear in the Main file (1.1% as billers). In the IE, 4,292 of 5,035 appear nowhere in Source 1.
- 860 are physician rows with no specialty.
- This is what ordering/referring/prescribing-only records would look like, so they were removed from b to e. **The expansion of "ORP" is [UNVERIFIED].**
- Source 2 rows carry no type or taxonomy.

**Limits.** Taxonomy rescue uses NUCC prefixes and may misassign subspecialists. Specialty 41 mixes primary care and hospitalists. Clinics and groups are counted separately from practitioners. Dental billing addresses are not service locations. [COMPUTED: s02_supply.py, s02b_supply_diagnostics.py]

## 9. HPSA vs FFS access

**Method.** Designated PC-HPSA tract components assigned to ZCTAs through the Census 2020 tract-ZCTA relationship (share of ZCTA land in designated tracts; 71 of 169 ZCTAs at 50% or more). Facility (point) designations are not counted as areas. "Proposed for withdrawal" is treated as not designated.

**Effect.**
- PC-HPSA ZCTAs have lower PC catchment (delta -0.60, 95% CI -0.76 to -0.43, BH p < 0.001; medians 1.41 vs 3.67, n = 130) and a lower raw ratio (-0.30, -0.50 to -0.07).
- **HPSA detects 70% of the lowest-quartile ZCTAs (33) with 78% specificity (kappa 0.43). Ten of 33 (111,824 of 300,163 eligibles) are not in a PC-HPSA**, and 21 PC-HPSA ZCTAs are not low.
- MH-HPSA vs MH catchment: -0.39 (-0.58 to -0.19).
- Dental HPSA vs dental catchment: -0.18 (-0.40 to 0.03; adj p 0.16, not significant, not evidence of none).
- HPSA score vs PC catchment among designated ZCTAs: rho -0.22 (-0.57 to 0.15, n = 44).

**Limits.** HPSA counts all providers and is population-based; the tract-ZCTA step uses land overlap. [COMPUTED: s05a_covariates.py, s05b_correlations.py]

## 10. Requested correlations

n = 130 unless noted. "Catchment" = fixed 30 km Gaussian (no RUCA, so the rurality test is not circular). Estimate = Spearman rho with bootstrap 95% CI. Adj p = BH across 69 tests. Weighted = eligibles-weighted rho.

| Test | Estimate (95% CI) | BH adj p | Weighted |
|---|---|---|---|
| Eligibles/km2 vs PC count | 0.50 (0.35 to 0.63) | < 0.001 | 0.40 |
| Eligibles/km2 vs raw EB ratio (partly mechanical) | 0.26 (0.10 to 0.41) | 0.006 | 0.24 |
| Eligibles/km2 vs PC catchment | 0.61 (0.48 to 0.71) | < 0.001 | 0.59 |
| Medi-Cal enrolment rate vs PC catchment | -0.15 (-0.32 to 0.02) | 0.13 | -0.09 |
| Poverty vs raw EB PC | -0.06 (-0.21 to 0.11) | 0.59 | 0.03 |
| Poverty vs PC catchment | -0.17 (-0.34 to 0.00) | 0.084 | -0.08 |
| Poverty vs MH catchment | -0.38 (-0.53 to -0.24) | < 0.001 | -0.34 |
| Poverty vs dental catchment | -0.34 (-0.49 to -0.17) | < 0.001 | -0.30 |
| Median income vs PC catchment | 0.28 (0.12 to 0.45) | 0.002 | 0.22 |
| RUCA vs raw EB PC | -0.26 (-0.41 to -0.10) | 0.006 | -0.23 |
| RUCA vs PC catchment | -0.58 (-0.68 to -0.46) | < 0.001 | -0.38 |
| RUCA vs MH catchment | -0.67 (-0.74 to -0.56) | < 0.001 | -0.44 |
| RUCA vs dental catchment | -0.74 (-0.80 to -0.65) | < 0.001 | -0.53 |
| Share 65+ vs PC catchment | -0.27 (-0.43 to -0.09) | 0.004 | -0.31 |
| Share 65+ vs cardiology catchment | -0.12 (-0.31 to 0.07) | 0.20 | -0.14 |
| Share 65+ vs endocrinology catchment | -0.14 (-0.33 to 0.05) | 0.14 | -0.10 |
| Women 15-44 vs OB/GYN catchment | 0.26 (0.07 to 0.44) | 0.005 | 0.31 |
| LEP vs raw EB PC | -0.03 (-0.20 to 0.15) | 0.76 | -0.08 |
| LEP vs PC catchment | 0.37 (0.20 to 0.52) | < 0.001 | 0.38 |
| LEP vs MH catchment | 0.37 (0.20 to 0.52) | < 0.001 | 0.34 |
| Vulnerability index* vs raw EB PC | -0.07 (-0.24 to 0.10) | 0.49 | -0.05 |
| Vulnerability index* vs PC catchment | -0.16 (-0.34 to 0.03) | 0.11 | -0.05 |
| Vulnerability index* vs MH catchment | -0.33 (-0.48 to -0.16) | < 0.001 | -0.29 |
| PC-HPSA vs raw (Cliff's d) | -0.30 (-0.50 to -0.07) | 0.009 | n/a |
| PC-HPSA vs PC catchment (Cliff's d) | -0.60 (-0.76 to -0.43) | < 0.001 | n/a |
| Dental HPSA vs dental catchment (Cliff's d) | -0.18 (-0.40 to 0.03) | 0.16 | n/a |

*Vulnerability index = poverty, no vehicle, uninsured, no checkup, disability and low income; LEP is excluded.

**Outliers.** Jackknife ranges are within about +/-0.03 of the estimate for most tests, so no single ZCTA drives them. The 65+ tests move most when the extreme 5% of x is dropped (cardiology -0.12 to -0.31; all specialists -0.08 to -0.27), so those nulls are fragile. Eligibles weighting attenuates the rurality and poverty effects because the affected ZCTAs are small.

**Reading (nulls and negatives first).**
- **Poverty vs PC supply:** null for the raw ratio, weak non-significant negative for catchment. It is clearly negative for mental-health and dental catchment. A 130-ZCTA sample cannot exclude a modest PC association.
- **LEP:** null for the raw ratio, but positive for catchments (dense areas have more accessible supply). Language concordance is invisible in E.
- **Age vs specialty:** older ZCTAs do not have more cardiology access (-0.12, not significant); they have somewhat less primary-care access.
- **Vulnerability vs shortage:** null for PC, negative for mental health.
- **Rurality** is negative for every category and weaker for the raw ratio.
- **Density:** provider counts rise with eligibles. The ratio's positive association is partly mechanical.

## 11. Models and spatial dependence

**NB count model, PC count (b), offset log eligibles, n = 130.** Poisson dispersion 192 (overdispersed), NB alpha 1.91, residual Moran's I 0.02 (p 0.27), 7 ZIP3 clusters, so clustered p-values are optimistic (HC1 shown beside). VIFs are at most 1.9.

| Term | Rate ratio (95% CI) | p cluster | BH adj p | p HC1 |
|---|---|---|---|---|
| Poverty, per pp | 0.93 (0.88 to 0.98) | 0.008 | 0.018 | 0.020 |
| LEP, per pp | 0.94 (0.88 to 1.00) | 0.037 | 0.071 | 0.032 |
| Age 65+, per pp | 1.05 (1.04 to 1.06) | < 0.001 | < 0.001 | 0.033 |
| No vehicle, per pp | 1.39 (1.24 to 1.56) | < 0.001 | < 0.001 | < 0.001 |
| log pop. density | 1.95 (1.57 to 2.41) | < 0.001 | < 0.001 | < 0.001 |
| Non-metro | 0.91 (0.35 to 2.35) | 0.85 | 0.91 | 0.84 |
| FQHC site present | 2.73 (1.64 to 4.56) | < 0.001 | 0.001 | 0.001 |

Mental-health and specialist count models (same covariates) are in `s05_models.csv`. They are qualitatively similar, except non-metro specialists (RR 1.8, p 0.038 clustered but 0.41 HC1, so not robust).

**OLS on log PC catchment (30 km).** R2 0.40. Only log density is clearly significant (+34%, BH p < 0.001); no-vehicle +5.6% per pp (BH adj p 0.07, cluster p 0.039). Residual Moran's I 0.49 (p 0.001), so standard errors are too small and the model is descriptive. Weighted and unweighted agree for density and diverge for no-vehicle (0.054 vs 0.013).

**Moran's I (n = 130, queen contiguity, 999 permutations).**

| Variable | I | BH adj p |
|---|---|---|
| EB PC per 1,000 | 0.05 | 0.086 |
| PC catchment | 0.83 | 0.001 |
| MH catchment | 0.80 | 0.001 |
| Poverty | 0.38 | 0.001 |
| Vulnerability | 0.32 | 0.001 |
| Diabetes | 0.36 | 0.001 |

LISA on PC catchment: 36 high-high (Inland valley core) and 27 low-low ZCTAs at p < 0.05, and the same 36 and 27 survive BH q = 0.10. LISA on the raw ratio finds only 3 low-low ZCTAs after BH (at raw p < 0.05: 4 high-high, 6 low-low, 1 high-low, 3 low-high). [COMPUTED: s05b_correlations.py]

## 12. Base table, ZIP vs ZCTA, and the roughly 3% gap

**Base table.** 169 ZCTAs touch Riverside or San Bernardino. 168 are in A for 2026-09; 89019 is mostly Nevada. `zip` and `zcta` are separate 5-character text columns. Counts are given for 2026-09 (primary), 2026-08 and 2025-09 (final). The month changes levels, not ranks: ZCTA eligibles rho 0.9999 (vs 08) and 0.9991 (vs 2025-09), raw-ratio ranks 0.9998 or higher, and eligibles are 8.0% lower in the two counties in 2026-09.

**County rule.** Each ZCTA goes to the county with the largest *estimated population* share: Census 2020 tract populations x tract-ZCTA land overlap (uniform density within a tract), with land-area majority as the fallback. 71 ZCTAs are assigned to Riverside, 93 to San Bernardino (including 89019, which is not in A) and 5 to other counties (91759 and 91766 Los Angeles, 92028 San Diego, 93516 and 93555 Kern). Two differ from land-area assignment (92397; 89019).

Split ZCTAs are flagged (`is_split_zcta`) at 10% or more of estimated population outside the assigned county:
- 91759 (41%; 85 eligibles)
- 92274 (15%)
- 92373 (12%)

Two more are at 5% or more: 91766 (5.8%) and 92324 (5.4%). The data report's "19 split ZCTAs" counts any land overlap; by population only three are material. Land-area splitting would say 92277 is 78% San Bernardino by land, which says nothing about where people live.

**Reconciliation, 2026-09, all Medi-Cal eligibles:**

| County | B total | A, ZCTAs assigned by population-majority rule | A, split by population share | A, split by land area |
|---|---|---|---|---|
| Riverside | 912,055 | 904,764 | 904,330 | 909,642 |
| San Bernardino | 905,173 | 908,744 | 908,515 | 897,149 |

The guide's route (sum A over every ZCTA touching either county) gives 1,871,886 vs B's 1,817,228 (**+3.01%**; +3.0% in 2026-08 and +3.1% in 2025-09). About 59,042 members live outside the two counties in split ZCTAs. Allocating each ZCTA's eligibles by estimated population share leaves a residual of 4,384 (0.24% of B). Land-area allocation is worse. The remainder is ZIPs without ZCTA, the 162,125 statewide members whose ZIP is "." and cannot be placed, suppressed cells, and the uniform-density assumption. These allocations spread *all* eligibles by total population share; they are not status-specific and are not used for demand.

**ZIPs without a ZCTA.**
- Statewide in A 2026-09, 757 of 2,554 ZIPs (15,394 members) have no ZCTA. 22 of them are in the IE (7,687 members), mostly PO-box-type ZIPs; the largest is 4,906.
- Separately, five ZCTAs touching the IE have no gazetteer point and no polygon (92317, 92350, 92369, 92415, 92521). They hold 14,859 eligibles; 92415 alone is 14,573 (0.8% of the IE total) and cannot be located.
- These members are in the base table but in no catchment or ranking.

**Suppression.** Five ZCTAs have a suppressed 2026-09 Total (92278, 92304, 92338, 92280, 92364), plus 89019 (absent). Suppressed is not zero; bounds 1-10 are stored; none is ranked. [COMPUTED: s01_base_table.py, s07_quality.py]

## Findings nobody asked for

1. **E is not a selective list** (finding 3): physician NPIs match the all-payer count, and PC physicians exceed it by a quarter. A "providers per 1,000 eligibles" ratio mostly measures where physicians are.
2. **Hospital-campus addresses drive the raw ratio.** 43% of PC records sit at 100+-NPI addresses; 7 of 164 ZCTAs hold half; capping alone cuts PC by 37%. The best-looking ZCTAs by the guide's ratio are campuses (128 vs 5.9 for Loma Linda).
3. **35% of IE ZCTAs (6% of eligibles) have no PC record at all.** Eligibles are far less concentrated than records (Gini 0.55 vs 0.83).
4. **The raw ratio hides the desert gap.** Non-metro vs metro delta is -0.09 (not significant) for the raw ratio vs -0.71 for catchment. Raw and catchment ranks agree at rho 0.34 to 0.41.
5. **FQHC sites sit where supply is, not where it is thin.** ZCTAs with a HRSA site have higher PC catchment (delta +0.23, adj p 0.041), 2.7x more PC records per eligible after adjustment, and higher poverty (rho +0.26, adj p 0.005). They co-locate with other supply rather than substitute for it. Caveat: FQHC-employed clinicians are inside the PC counts, so part of this is mechanical.
6. **Need and supply are mismatched.** A chronic-need index (diabetes, heart disease, no checkup, depression; CDC PLACES) is negatively related to PC catchment (rho -0.45, CI -0.59 to -0.28, adj p < 0.001); depression vs MH catchment -0.54. "No routine checkup" runs the other way (+0.27), which I cannot explain.
7. **No-vehicle households do not cluster where catchment access is low** (rho 0.00 at 30 km, +0.07 at 15 km; null, not evidence of absence). They correlate +0.21 with the raw ratio because dense cores have more records and more households without cars.
8. **No Simpson-type reversal for poverty.** Raw -0.06 and catchment -0.17 have the same sign pooled and within strata (Riverside -0.27, p 0.027; San Bernardino -0.12). The pictures do disagree for LEP (null vs +0.37) and rurality (weak vs strong).
9. **The ranking is far less sensitive to demand assumptions than to supply and weights**, so the uniform-share worry is smaller than the "what does E count" worry.
10. **Provider_Source 3 looks ordering/referring-only** (all non-billing, no flag, 84% absent from the Main file) and Source 2 is untyped; together 13% of IE rows. Including them would inflate supply by about 1,400 candidate PC-or-NP rows.
11. **Denominators are moving.** Eligibles are down 8.0% in a year, managed care down 7.7%, FFS flat; the 2026-09 FFS count is about 12% low.
12. **Kaiser outnumbers Molina** in the two counties (189,300 vs 151,975 in B 2026-09), the reverse of the Dec-2024 split.
13. **Mental-health supply in FFS-enrolled counts is not short** vs neighbours (1.31x) while specialists and cardiology are; many of those records are therapists whose FFS acceptance is invisible.
14. **One PO-box-type ZIP (92415) holds 14,573 eligibles that cannot be located**, and the Census relationship file lists ZCTAs with no polygon.

## What cannot be determined from public data

- Where transitioning members live (by design); county counts; IEHP's 100,000 vs 132,000 figure and whether it includes QNC; Molina and Kaiser mover counts [UNVERIFIED].
- Who accepts new FFS patients. E has no claims, there is no audit of FFS lists, and the self-reported flag covers 4.4% of rows. Effective capacity, dormancy by area, panel headroom and waits are unobserved.
- Groups A, B and C. They need IEHP's NPI-level directory, which was not downloaded.
- Travel time, transit and language concordance (straight-line proxy only).
- Older vintages of A and B, so the size of the upward revision to 2026-09 FFS is bounded only indirectly.
- The expansion of "ORP", what Source 2 ("NMP") means, and whether Source 3 providers can bill.
- Out-of-state demand for border providers, so the Colorado River ZCTAs are not reliably measured.
- Within-ZCTA distribution of eligibles for the 757 ZIPs without ZCTA and the five ZCTAs without polygons.
- Cause. Every association here is cross-sectional, ZCTA-level and spatially autocorrelated; none describes individuals.

## Method notes and reproduction

- Steps: `s01` geography, base table and reconciliation; `s02` and `s02b` classification, definitions a-e, concentration, ORP and CHCF checks; `s03` raw ratio with empirical Bayes and two-step catchment; `s04` scenarios and flag; `s05a` and `s05b` covariates and correlations; `s06` ranking and stability; `s07` quality; `s08` figures.
- Figures: f1 definitions; f2 raw vs catchment; f3 Lorenz; f4 maps; f5 tiers; f6 stability; f7 extra patients per provider; f8 flag; f9 correlation forest; f10 E vs CHCF; f11 all-plan movers.
- Tests: `$HOME/.venvs/iehp-access/bin/python -I tests/test_analysis_outputs.py`. 15 assertions: keys, data-report counts, guide rounding, reconciliation, definition nesting, ORP exclusion, denominator identity, sensitive-column guard.
