# IEHP Access to Care Analysis

Cal Poly Pomona CEO Business Challenge: how the January 1, 2027 move of some Medi-Cal members from
managed care to fee-for-service affects Inland Empire Health Plan members in Riverside and San Bernardino counties.

**Status: Phase 0, research in progress.** Findings are preliminary and have not had independent review.
Rules for this work are in `docs/phase0_contract.md`. Read them before adding any analysis, especially the
sensitive-population rules.

## Set up on a new machine

```bash
git clone https://github.com/BrooklynD23/CEO-Business-Challenge.git
cd CEO-Business-Challenge
UV_PROJECT_ENVIRONMENT="$HOME/.venvs/iehp-access" uv sync
```

Four raw files exceed GitHub's 100 MB limit and are not in this repo (see `.gitignore`):

- `data/raw/E_ffs_providers/medi-cal-ffs-provider-listing_10_26_26.csv`
- `data/raw/X_acs5_zcta/acsdt5y2024-b01001.dat`
- `data/raw/X_acs5_zcta/acsdt5y2024-b17001.dat`
- `data/raw/X_acs5_zcta/acsdt5y2024-b27001.dat`

Restore them with:

```bash
"$HOME/.venvs/iehp-access/bin/python" -I scripts/download_data.py --only E X_acs
```

Files already on disk are skipped. Publishers update their files, so compare a re-download against the SHA-256
values in `data/catalog/download_manifest.csv`. The analysis used the 2026-10-26 FFS provider listing.

## Where things are

| Path | Contents |
|---|---|
| `research/policy_verification.md` | What the transition policy says, checked against primary sources |
| `research/intervention_evidence.md` | Evidence and costs for candidate interventions |
| `research/data_acquisition_report.md` | What each dataset contains, and its traps |
| `research/analysis_findings.md` | Statistical findings |
| `scripts/analysis/` | Analysis pipeline |
| `data/catalog/` | Dataset inventory, data dictionary, download manifest |
