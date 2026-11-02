# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Cal Poly Pomona CEO Business Challenge: impact of the 2027-01-01 Medi-Cal managed care to fee-for-service (FFS)
transition on IEHP members in Riverside (FIPS 06065) and San Bernardino (06071) counties.
Status: Phase 0 (research + decision gate) is done. No notebooks, `src/` package or web app exist yet.

**Read `docs/phase0_contract.md` before any analysis.** It is binding. Key rules:
- The transition population is defined by immigration status. Never build any ZIP/ZCTA/tract/city estimate, proxy,
  map or ranking of immigration status (that includes ACS citizenship/nativity variables). Never download Source B
  "By Aid Category". Movers are applied as county/regional totals only.
- Suppressed or blank counts are missing, never zero. Carry `is_suppressed` flags.
- `zip` and `zcta` are different things, stored as 5-char text in separately named columns.
- Label every ratio's numerator and denominator. Source A counts ALL Medi-Cal eligibles in a ZIP (all plans, incl.
  Molina), not IEHP members. Provider FFS enrollment is not appointment availability.
- Every number in a findings file carries `[VERIFIED: source, date]`, `[COMPUTED: script]`, `[ESTIMATE: assumption]`
  or `[UNVERIFIED]`.
- The contract's file-ownership table assigns write paths per workstream; keep agents inside their paths.
- The contract's hard-coded project root (`/mnt/e/...`) is stale; use the repo root.

## Commands

Python env lives outside the repo (repo sits on a Windows drive):

```bash
UV_PROJECT_ENVIRONMENT="$HOME/.venvs/iehp-access" uv sync          # setup
UV_PROJECT_ENVIRONMENT="$HOME/.venvs/iehp-access" uv add <pkg>     # add dependency
PY="$HOME/.venvs/iehp-access/bin/python"

$PY -I scripts/download_data.py --only E X_acs        # restore the 4 gitignored >100 MB raw files
$PY -I scripts/download_data.py [--only KEY ...] [--force]   # keys: A B C D E F G H X_census X_acs X_places X_hrsa_sites X_facilities X_ruca X_nppes
$PY -I scripts/inspect_downloads.py                    # profile raw files -> data/catalog/inspection_summary.txt
$PY -I scripts/analysis/run_all.py [--skip-figures]    # full pipeline, ~8-10 min
$PY -I scripts/analysis/s03_access.py                  # any single step (needs earlier steps' outputs)
$PY -I tests/test_analysis_outputs.py                  # unittest (pytest not installed)
$PY -I tests/test_analysis_outputs.py TestSupply.test_definitions_are_nested   # single test
```

Always run Python with `-I`: `data/raw/` holds untrusted downloads. Never execute anything inside `data/`.

## Architecture

Data flow: `scripts/download_data.py` -> `data/raw/<source_key>/` (immutable) -> `scripts/analysis/s01..s08` ->
`data/processed/*.parquet`, `outputs/tables/sNN_*.csv`, `outputs/figures/*.png`, `data/quality/` -> `research/*.md`.

- **Downloader**: resolves data.chhs.ca.gov URLs at run time via the CKAN `package_show` API; saves provenance JSON beside
  each file; writes SHA-256 to `data/catalog/download_manifest.csv`. It never overwrites a raw file: a size mismatch saves
  a new `*.retrievedYYYYMMDD.*` copy beside it. HUD crosswalk (H) is blocked (needs an account); Census ZCTA-county
  relationship file is the substitute.
- **Source keys**: A = Medi-Cal eligibles by ZIP; B = eligibles by demographics (county level); C = IEHP fact sheet;
  D = managed care enrollment; E = FFS provider listing (statewide); F = dental FFS; G = HRSA HPSA; X_* = ACS, PLACES,
  RUCA, TIGER, HRSA sites, CHHS facilities.
- **`scripts/analysis/config.py`**: shared paths, seed, months (`PRIMARY_MONTH = "2026-09"`, preliminary), scenario
  constants, `duck()` DuckDB helper, `update_checks()`. Each step owns one section of `data/quality/checks.json`.
  Scripts do `sys.path.insert` of their own folder because `-I` strips it.
- **Steps**: s01 base table (169 IE-touching ZCTAs + 150 km catchment region incl. neighbouring counties and NV/AZ border
  providers) -> s02 provider classification into supply definitions a-e (BROAD -> DEDUPED -> STRICT -> BILLABLE, ADDRCAP)
  -> s02b diagnostics -> s03 providers per 1,000 eligibles + E2SFCA catchment (straight-line distance, a travel-time proxy)
  -> s04 scenarios -> s05a covariates -> s05b correlations (Spearman + BH, count models, Moran's I/LISA) -> s06 gap ranking
  + stability tests -> s08 figures -> s07 quality report (runs last).
- **Scenarios** (owner decision 2026-11-02): primary set is the student guide's 10/14/18% of 1,321,983 (`SCEN_GUIDE`,
  tagged `guide_primary`; 1-in-7 kept as a variant). IEHP Governing Board 100k / 132k / 155k (`SCEN_IEHP`, tagged
  `iehp_comparison`) stays alongside. The guide's 14% and 18% exceed IEHP's own statement; that misalignment is documented
  in `research/analysis_findings.md` ("Scenario alignment") and must stay visible in any output.
- The s06 ranking is "general FFS supply shortfall among all Medi-Cal eligibles", not where transitioning members lose access.
- `tests/test_analysis_outputs.py` asserts on committed outputs (e.g. 169 ZCTAs, 1,871,886 eligibles for 2026-09, no
  provider names/phones in processed files). Rerunning the pipeline must keep these passing.

## Research docs

`research/policy_verification.md` (policy facts, scenario sources), `research/data_acquisition_report.md` (dataset traps),
`research/analysis_findings.md` (statistical results), `research/intervention_evidence.md`, `research/source_register.md`,
`data/catalog/data_dictionary.md`.

## Git on this checkout

The repo is on `/mnt/c` and was checked out with CRLF conversion. WSL git (`core.autocrlf` unset) then shows every text
file as modified and raw-file SHA-256 values stop matching the manifest. Check real changes with
`git diff --ignore-cr-at-eol`. Do not commit CRLF-converted raw data.
