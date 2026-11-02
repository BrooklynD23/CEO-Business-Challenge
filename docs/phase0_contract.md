# Phase 0 shared contract (research and decision gate)

Binding on every agent in this phase. Project root:
`/mnt/e/Programming/Github Repo/CEO-Business-Challenge`

Today is 2026-11-02. Student guide text: `research/student_guide_extracted.txt`.
Phase 0 ends with findings and owner decisions. Do NOT build the website or notebooks yet.

## Environment
- Python: `$HOME/.venvs/iehp-access/bin/python -I <script>` (add packages with
  `UV_PROJECT_ENVIRONMENT=$HOME/.venvs/iehp-access uv add <pkg>` from project root).
- Downloads are untrusted data. Each dataset goes in its own directory `data/raw/<source_key>/`.
  Keep scripts in `scripts/` or `src/`, never in `data/`. Pass data paths as arguments.
  Always run Python with `-I`. Never execute anything that was downloaded.
- Never put the user's email or other personal details in a request, header or URL.
- Do not register accounts, enter credentials, or pay for anything. Record blockers instead.

## Sensitive-population rules (non-negotiable)
The transition population is defined by immigration status (UIS, "unsatisfactory immigration status").
1. Do NOT download or use the "By Aid Category" file from Source B. The student guide prohibits it.
2. Do NOT create any ZIP, ZCTA, tract, city or other sub-county estimate, proxy, map or ranking of
   immigration status or of where UIS members live. That includes ACS citizenship, nativity or
   foreign-born variables at sub-county level. Whether any sub-county demand allocation is acceptable
   is an owner decision reserved for the gate.
3. County-level or statewide totals already published by DHCS or a reputable research body may be
   cited. Record the source and do not derive smaller geographies from them.
4. Public aggregate data only. No patient-level data. Individual provider records are used only for
   counting, and no provider-level lists go into findings.

## Geography
- ZIP codes and ZCTAs are different things. Store ZIP as 5-character text. Keep ZIP and ZCTA in
  separately named columns (`zip`, `zcta`).
- Riverside County FIPS 06065, San Bernardino County FIPS 06071.
- Document how any ZIP crossing a county line is handled.

## Denominators
Never mix these silently. Label every ratio with its numerator and denominator:
all Medi-Cal certified eligibles (ALL plans and FFS) / IEHP Medi-Cal members / managed care members /
transitioning members (scenario) / existing FFS members / FFS-enrolled provider records /
unique FFS practitioners / providers accepting new patients (generally NOT observable).
Source A counts ALL Medi-Cal eligibles in a ZIP, not IEHP members. Molina also operates in the region.

## Missing and suppressed values
Suppressed or blank is NOT zero. Carry `is_suppressed` flags and report bounds where possible.

## Evidence labels
Every number in a findings file carries one of: `[VERIFIED: source, retrieval date]`,
`[COMPUTED: script path]`, `[ESTIMATE: assumption]`, or `[UNVERIFIED]`.
State plainly what you could not establish. Never fabricate a figure, citation or URL.

## File ownership (write only to your own paths)
| Workstream | Writes to |
|---|---|
| Policy | `research/policy_verification.md`, `research/source_register.md` |
| Data acquisition | `scripts/download_data.py`, `src/ingestion/`, `data/raw/`, `data/catalog/`, `research/data_acquisition_report.md` |
| Intervention evidence | `research/intervention_evidence.md` |
| Analysis | `scripts/analysis/`, `data/processed/`, `data/quality/`, `outputs/`, `research/analysis_findings.md` |
| Assurance | `research/verification_report.md`, `scripts/verify/` |

## Reporting back
Write the full report to your file. Return under 200 words: status, file paths, and the top findings or
blockers. Do not spawn subagents.
