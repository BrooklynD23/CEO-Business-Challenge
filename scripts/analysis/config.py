"""Shared paths, constants and helpers for the Phase 1 access-to-care analysis.

Run every script with:  $HOME/.venvs/iehp-access/bin/python -I scripts/analysis/<script>.py
(-I removes the script folder from sys.path, so each script inserts it explicitly.)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
QUAL = ROOT / "data" / "quality"
TAB = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
for _p in (PROC, QUAL, TAB, FIG):
    _p.mkdir(parents=True, exist_ok=True)

SEED = 20261102

RIV, SB = "06065", "06071"
IE_FIPS = (RIV, SB)
COUNTY_NAMES = {
    "06065": "Riverside", "06071": "San Bernardino", "06037": "Los Angeles", "06059": "Orange",
    "06073": "San Diego", "06025": "Imperial", "06029": "Kern", "06027": "Inyo", "06111": "Ventura",
    "06083": "Santa Barbara", "06079": "San Luis Obispo", "06019": "Fresno", "06107": "Tulare",
    "06051": "Mono", "06009": "Calaveras", "06115": "Yuba",
}

# Months used from source A / B
PRIMARY_MONTH = "2026-09"      # preliminary (P); primary per data report
SENS_MONTHS = ["2026-08", "2025-09"]   # 2026-08 preliminary; 2025-09 final
ALL_MONTHS = [PRIMARY_MONTH] + SENS_MONTHS

# IEHP / scenario constants
IEHP_MEDICAL_FACTSHEET = 1_321_983          # [VERIFIED: C fact sheet Oct 2026]
IEHP_ALL_PROGRAMS = 1_394_246
# COMPARISON set (policy_verification.md section 2): IEHP Governing Board 2026-08-10. Owner chose SCEN_GUIDE as primary on 2026-11-02.
SCEN_IEHP = {"Low (IEHP 'more than 100,000')": 100_000,
                "Mid (IEHP 'about 10%' of Medi-Cal)": 132_000,
                "High (10% of all members + ~15k QNC; may double count)": 155_000}
# PRIMARY set (owner decision 2026-11-02): student guide scenarios (14% and 18% exceed IEHP stated figure)
SCEN_GUIDE = {"Guide low 10%": 0.10, "Guide mid 14.0%": 0.14, "Guide mid 1-in-7": 1 / 7, "Guide high 18%": 0.18}

ACCEPT_LO, ACCEPT_HI = 0.40, 0.65     # research/intervention_evidence.md section 2.2

# Neighbouring-county FIPS that the catchment must include (they fall inside the 150 km buffer)
NEIGHBOR_FIPS = ["06037", "06059", "06073", "06025", "06029", "06027"]
BUFFER_KM = 150.0

EVIDENCE = {
    "COMPUTED": "[COMPUTED: {}]",
}


def sys_path_fix():
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)


def num(col: str) -> str:
    """DuckDB SQL expression turning a text count with commas/spaces into BIGINT (NULL if blank)."""
    return f"try_cast(replace(replace(trim({col}), ',', ''), ' ', '') as bigint)"


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2, default=str)


def read_json(path: Path, default=None):
    if path.exists():
        with open(path) as fh:
            return json.load(fh)
    return default


def update_checks(section: str, payload: dict) -> None:
    """Merge a section into data/quality/checks.json (each script owns one section)."""
    p = QUAL / "checks.json"
    d = read_json(p, {})
    d[section] = payload
    write_json(p, d)


def duck():
    import duckdb
    con = duckdb.connect()
    con.execute("PRAGMA threads=16")
    return con


def rel(path) -> str:
    return str(Path(path).resolve().relative_to(ROOT))
