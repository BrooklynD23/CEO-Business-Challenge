#!/usr/bin/env python
"""Download public source data for the IEHP access-to-care analysis (Phase 0).

Run:  $HOME/.venvs/iehp-access/bin/python -I scripts/download_data.py [--only KEY ...] [--force]

Design rules (docs/phase0_contract.md):
  * Files land unchanged in data/raw/<source_key>/ and are never edited or deleted afterwards.
  * Resource URLs for data.chhs.ca.gov are resolved at run time via the CKAN package_show API.
  * Re-runnable and idempotent: an existing file whose size matches the remote size is kept
    ("cached"). If the remote file has changed size, the new version is saved beside the old
    one with a retrieval-date suffix; the old file is never overwritten.
  * Large files are streamed to disk and hashed on the fly.
  * Plain descriptive User-Agent, no personal details, no API keys, no accounts.
  * Source B "By Aid Category" (and the B "All resource data" ZIP that bundles it) is never
    requested. A hard guard in `pick_b_resources` enforces this.
  * Source H (HUD USPS crosswalk) needs an account: recorded as a blocker, never requested.
Output: data/catalog/download_manifest.csv
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CATALOG = ROOT / "data" / "catalog"
MANIFEST = CATALOG / "download_manifest.csv"
MANIFEST_COLS = ["source_key", "url", "retrieved_at", "sha256", "bytes", "status", "blocker",
                 "local_path", "note"]

UA = "PublicHealthAccessResearch/1.0 (academic analysis of public Medi-Cal data; plain script)"
CKAN = "https://data.chhs.ca.gov/api/3/action/package_show?id="
TIMEOUT = (30, 180)
CHUNK = 1 << 20

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept": "*/*"})

MANIFEST_ROWS: dict[tuple[str, str], dict] = {}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def load_manifest() -> None:
    if MANIFEST.exists():
        with MANIFEST.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                MANIFEST_ROWS[(row["source_key"], row["url"])] = row


def save_manifest() -> None:
    CATALOG.mkdir(parents=True, exist_ok=True)
    rows = sorted(MANIFEST_ROWS.values(), key=lambda r: (r["source_key"], r["url"]))
    tmp = MANIFEST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in MANIFEST_COLS})
    tmp.replace(MANIFEST)


def record(key: str, url: str, **kw) -> dict:
    row = {c: "" for c in MANIFEST_COLS}
    row.update(source_key=key, url=url, retrieved_at=kw.pop("retrieved_at", now()))
    row.update({k: ("" if v is None else str(v)) for k, v in kw.items()})
    MANIFEST_ROWS[(key, url)] = row
    save_manifest()
    return row


def get_json(url: str, tries: int = 3) -> dict:
    last = None
    for i in range(tries):
        try:
            r = SESSION.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"GET {url} failed: {last}")


def get_text(url: str, tries: int = 3) -> str:
    last = None
    for i in range(tries):
        try:
            r = SESSION.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            return r.text
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"GET {url} failed: {last}")


def remote_size(url: str) -> int | None:
    try:
        # identity encoding: with gzip a HEAD can report the size of an empty gzip body (20 bytes)
        r = SESSION.head(url, timeout=TIMEOUT, allow_redirects=True, headers={"Accept-Encoding": "identity"})
        n = int(r.headers.get("content-length") or 0)
        if r.status_code == 200 and n > 1024 and "content-encoding" not in r.headers:
            return n
    except Exception:  # noqa: BLE001
        pass
    return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def looks_like_html(head: bytes) -> bool:
    s = head.lstrip()[:200].lower()
    return s.startswith(b"<!doctype html") or s.startswith(b"<html")


def fetch(key: str, url: str, filename: str, *, note: str = "", expect_html: bool = False,
          force: bool = False) -> bool:
    """Stream url -> data/raw/<key>/<filename>. Returns True if a usable file is on disk."""
    outdir = RAW / key
    outdir.mkdir(parents=True, exist_ok=True)
    dest = outdir / filename
    prev = MANIFEST_ROWS.get((key, url))
    rsize = remote_size(url)

    if dest.exists() and dest.stat().st_size > 0 and force:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
        dest = outdir / f"{dest.stem}.retrieved{stamp}{dest.suffix}"
        log(f"{key}: --force: saving a fresh copy as {dest.name} (original kept)")
    elif dest.exists() and dest.stat().st_size > 0:
        local = dest.stat().st_size
        known_ok = prev and prev.get("status") in ("ok", "cached") and prev.get("sha256")
        if rsize is None or rsize == local:
            sha = prev["sha256"] if known_ok and int(prev.get("bytes") or -1) == local else sha256_file(dest)
            record(key, url, retrieved_at=(prev or {}).get("retrieved_at") or now(), sha256=sha,
                   bytes=local, status="cached", blocker="", local_path=str(dest.relative_to(ROOT)),
                   note=note)
            log(f"{key}: cached {dest.name} ({local:,} B)")
            return True
        # remote changed: keep old file, save new one with date suffix
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        dest = outdir / f"{dest.stem}.retrieved{stamp}{dest.suffix}"
        log(f"{key}: remote size {rsize:,} != local {local:,}; saving new copy as {dest.name}")

    part = dest.with_suffix(dest.suffix + ".part")
    last_err = ""
    for attempt in range(3):
        try:
            h = hashlib.sha256()
            n = 0
            head = b""
            with SESSION.get(url, stream=True, timeout=TIMEOUT) as r:
                if r.status_code != 200:
                    last_err = f"HTTP {r.status_code}"
                    if r.status_code in (401, 403, 404, 410):
                        break
                    time.sleep(3 * (attempt + 1))
                    continue
                with part.open("wb") as fh:
                    for chunk in r.iter_content(CHUNK):
                        if not chunk:
                            continue
                        if not head:
                            head = chunk[:512]
                        fh.write(chunk)
                        h.update(chunk)
                        n += len(chunk)
            if n == 0:
                last_err = "empty response"
                continue
            if not expect_html and looks_like_html(head):
                last_err = "server returned an HTML page instead of the data file"
                part.unlink(missing_ok=True)
                break
            part.replace(dest)
            record(key, url, sha256=h.hexdigest(), bytes=n, status="ok", blocker="",
                   local_path=str(dest.relative_to(ROOT)), note=note)
            log(f"{key}: downloaded {dest.name} ({n:,} B)")
            return True
        except Exception as e:  # noqa: BLE001
            last_err = f"{type(e).__name__}: {e}"
            time.sleep(3 * (attempt + 1))
    part.unlink(missing_ok=True)
    record(key, url, status="failed", blocker=last_err, note=note)
    log(f"{key}: FAILED {url} -> {last_err}")
    return False


def blocked(key: str, url: str, blocker: str, note: str = "") -> None:
    record(key, url, status="blocked", blocker=blocker, note=note)
    log(f"{key}: BLOCKED {blocker}")


def ckan_package(key: str, slug: str) -> dict | None:
    """Resolve a CKAN dataset and save the package_show JSON as provenance."""
    url = CKAN + slug
    try:
        pkg = get_json(url)["result"]
    except Exception as e:  # noqa: BLE001
        record(key + "__ckan_metadata", url, status="failed", blocker=str(e))
        log(f"{key}: CKAN lookup failed: {e}")
        return None
    outdir = RAW / key
    outdir.mkdir(parents=True, exist_ok=True)
    meta = outdir / "_ckan_package_show.json"
    body = json.dumps(pkg, indent=1, sort_keys=True).encode()
    meta.write_bytes(body)  # provenance snapshot, rewritten each run (metadata, not source data)
    record(key + "__ckan_metadata", url, sha256=hashlib.sha256(body).hexdigest(), bytes=len(body),
           status="ok", local_path=str(meta.relative_to(ROOT)),
           note=f"metadata_modified={pkg.get('metadata_modified')}")
    return pkg


def csv_resources(pkg: dict) -> list[dict]:
    return [r for r in pkg["resources"] if (r.get("format") or "").upper() == "CSV"]


def fname_from_url(url: str) -> str:
    return url.rsplit("/", 1)[-1].split("?")[0]


def save_datastore_fields(key: str, res: dict) -> None:
    """Save CKAN datastore field definitions (column labels and notes) as a data dictionary source."""
    if not res.get("datastore_active"):
        return
    url = f"https://data.chhs.ca.gov/api/3/action/datastore_search?resource_id={res['id']}&limit=0"
    try:
        body = json.dumps(get_json(url)["result"]["fields"], indent=1).encode()
    except Exception as e:  # noqa: BLE001
        record(key + "__datastore_fields", url, status="failed", blocker=str(e))
        return
    path = RAW / key / f"_datastore_fields_{res['id']}.json"
    path.write_bytes(body)
    record(key + "__datastore_fields", url, sha256=hashlib.sha256(body).hexdigest(), bytes=len(body),
           status="ok", local_path=str(path.relative_to(ROOT)),
           note=f"CKAN field definitions for resource '{res['name']}'")


def fetch_resource(key: str, res: dict, extra_note: str = "") -> bool:
    note = f"resource='{res['name']}'; ckan_id={res['id']}; ckan_last_modified={res.get('last_modified')}"
    if extra_note:
        note += "; " + extra_note
    ok = fetch(key, res["url"], fname_from_url(res["url"]), note=note, force=ARGS.force)
    save_datastore_fields(key, res)
    return ok


# --------------------------------------------------------------------------- sources
def src_A() -> None:
    key = "A_zip_eligibles_2020_recent"
    pkg = ckan_package(key, "medi-cal-certified-eligible-counts-by-month-of-eligibility-zip-code-and-sex")
    if not pkg:
        return
    want = "Calendar Years 2020 to the Most Recent Reportable Month"
    hits = [r for r in csv_resources(pkg) if r["name"].strip() == want]
    if len(hits) != 1:
        record(key, CKAN, status="failed", blocker=f"expected 1 resource named '{want}', found {len(hits)}")
        return
    fetch_resource(key, hits[0])


B_WANTED = {
    "B_age_sex": "By Age Group and Sex, Certified Eligibles",
    "B_language": "By Primary Language, Certified Eligibles",
    "B_delivery_plan": "By Delivery System and Plan, Certified Eligibles",
    "B_race_ethnicity": "By Race/Ethnicity and Age Group, Certified Eligibles",
}


def pick_b_resources(pkg: dict) -> dict[str, dict]:
    out = {}
    for k, name in B_WANTED.items():
        hits = [r for r in csv_resources(pkg) if r["name"].strip() == name]
        if len(hits) != 1:
            log(f"{k}: expected 1 resource '{name}', found {len(hits)}")
            continue
        r = hits[0]
        # Hard guard: never the Aid Category file or the bundle ZIP that contains it.
        blob = (r["name"] + " " + r["url"]).lower()
        if "aid" in blob and "categor" in blob or "aid_cat" in blob or r["url"].lower().endswith(".zip"):
            raise SystemExit(f"REFUSING Source B resource: {r['name']}")
        out[k] = r
    return out


def src_B() -> None:
    pkg = ckan_package("B_demographics_package", "medi-cal-certified-eligibles-with-demographics-by-month")
    if not pkg:
        return
    for k, r in pick_b_resources(pkg).items():
        fetch_resource(k, r)
    record("B_by_aid_category", "(not requested)", status="excluded_by_policy",
           blocker="Student guide and phase0 contract prohibit the By Aid Category file (immigration status). Not downloaded or opened.")


def src_C() -> None:
    fetch("C_iehp_factsheet",
          "https://www.iehp.org/content/dam/iehp-org/en/documents/about/fact-sheet/IEHP_Fact_Sheet.pdf",
          "IEHP_Fact_Sheet.pdf", note="plan-published PDF; count month not stated", force=ARGS.force)


def src_D() -> None:
    key = "D_managed_care_enrollment"
    pkg = ckan_package(key, "medi-cal-managed-care-enrollment-report")
    if not pkg:
        return
    for r in csv_resources(pkg):
        fetch_resource(key, r)


def src_E() -> None:
    key = "E_ffs_providers"
    pkg = ckan_package(key, "profile-of-enrolled-medi-cal-fee-for-service-ffs-providers")
    if not pkg:
        return
    for r in csv_resources(pkg):  # provider list + provider type + specialty code references
        fetch_resource(key, r)


def src_F() -> None:
    key = "F_dental_ffs_providers"
    pkg = ckan_package(key, "profile-of-enrolled-medi-cal-dental-fee-for-service-ffs-providers-and-safety-net-clinics-sncs")
    if not pkg:
        return
    for r in csv_resources(pkg):
        fetch_resource(key, r)


def src_G() -> None:
    base = "https://data.hrsa.gov/DataDownload/DD_Files/"
    for k, f in [("G_hpsa_primary_care", "BCD_HPSA_FCT_DET_PC.csv"),
                 ("G_hpsa_mental_health", "BCD_HPSA_FCT_DET_MH.csv"),
                 ("G_hpsa_dental", "BCD_HPSA_FCT_DET_DH.csv")]:
        fetch(k, base + f, f, note="HRSA Data Warehouse nightly extract; national file", force=ARGS.force)


def src_H() -> None:
    blocked("H_hud_zip_county_crosswalk", "https://www.huduser.gov/portal/datasets/usps_crosswalk.html",
            "HUD USPS ZIP-County crosswalk requires registering an account; contract forbids registering. "
            "Substitutes: H_census_zcta_county (Census 2020 ZCTA-county relationship file), county columns in A/E.")
    fetch("H_census_zcta_county",
          "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt",
          "tab20_zcta520_county20_natl.txt",
          note="Census 2020 ZCTA5-to-county relationship (pipe-delimited, land+water area overlap); ZCTA not postal ZIP",
          force=ARGS.force)


def src_X_census() -> None:
    fetch("X_tiger_zcta_2020", "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_zcta520_500k.zip",
          "cb_2020_us_zcta520_500k.zip", note="Cartographic boundary 2020 ZCTA 1:500k shapefile (zip)", force=ARGS.force)
    fetch("X_tiger_county_2020", "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_500k.zip",
          "cb_2020_us_county_500k.zip", note="Cartographic boundary 2020 county 1:500k shapefile (zip)", force=ARGS.force)


ACS_YEAR_CANDIDATES = [2025, 2024, 2023]
# Tables chosen for access/need context. Deliberately NO citizenship, nativity, foreign-born
# or place-of-birth tables (contract sensitive-population rule 2).
ACS_TABLES = {
    "b01003": "Total population",
    "b01001": "Sex by age (age bands)",
    "b17001": "Poverty status by sex by age",
    "c16001": "Language spoken at home by ability to speak English (LEP by language group)",
    "b08201": "Household size by vehicles available (no-vehicle households)",
    "b27001": "Health insurance coverage status by sex by age (uninsured)",
    "b19013": "Median household income",
}


def src_X_acs() -> None:
    key = "X_acs5_zcta"
    year = None
    for y in ACS_YEAR_CANDIDATES:
        base = f"https://www2.census.gov/programs-surveys/acs/summary_file/{y}/table-based-SF/"
        try:
            r = SESSION.head(base + "documentation/Geos" + f"{y}5YR.txt", timeout=TIMEOUT, allow_redirects=True)
            if r.status_code == 200:
                year = y
                break
        except Exception:  # noqa: BLE001
            pass
    if year is None:
        record(key, "https://www2.census.gov/programs-surveys/acs/summary_file/", status="failed",
               blocker="no ACS 5-year table-based summary file found for candidate years")
        return
    log(f"ACS 5-year latest vintage with table-based summary file: {year} ({year-4}-{year})")
    base = f"https://www2.census.gov/programs-surveys/acs/summary_file/{year}/table-based-SF/"
    note0 = (f"ACS {year-4}-{year} 5-year table-based summary file, national, all geographies "
             "(ZCTA rows have GEO_ID 860Z200US#####). The keyless Census API now returns 'Missing Key', so "
             "bulk files are used instead.")
    for doc in (f"documentation/Geos{year}5YR.txt", f"documentation/ACS{year}5YR_Table_Shells.txt",
                "documentation/README.txt"):
        fetch(key, base + doc, f"ACS{year}_" + fname_from_url(doc), note="documentation; " + note0, force=ARGS.force)
    for t, desc in ACS_TABLES.items():
        fetch(key, base + f"data/5YRData/acsdt5y{year}-{t}.dat", f"acsdt5y{year}-{t}.dat",
              note=f"{desc}; {note0}", force=ARGS.force)


def src_X_places() -> None:
    key = "X_cdc_places_zcta"
    dsid = None
    name = None
    try:
        cat = get_json("https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&"
                       "q=PLACES%20ZCTA%20GIS%20Friendly%20Format&only=datasets&limit=30")
        best = (0, None, None)
        for item in cat["results"]:
            nm = item["resource"]["name"]
            m = re.fullmatch(r"PLACES: ZCTA Data \(GIS Friendly Format\), (\d{4}) release", nm)
            if m and int(m.group(1)) > best[0]:
                best = (int(m.group(1)), item["resource"]["id"], nm)
        _, dsid, name = best
    except Exception as e:  # noqa: BLE001
        log(f"PLACES catalog lookup failed: {e}")
    if not dsid:
        dsid, name = "kee5-23sr", "PLACES: ZCTA Data (GIS Friendly Format), 2025 release (fallback id)"
    log(f"PLACES dataset: {dsid} {name}")
    meta_url = f"https://data.cdc.gov/api/views/{dsid}.json"
    fetch(key, meta_url, f"{dsid}_metadata.json", note=f"Socrata view metadata (column descriptions) for {name}", force=ARGS.force)
    fetch(key, f"https://data.cdc.gov/api/views/{dsid}/rows.csv?accessType=DOWNLOAD", f"{dsid}_places_zcta.csv",
          note=f"{name}; model-based crude and age-adjusted prevalence per ZCTA, wide format", force=ARGS.force)


def src_X_hrsa_sites() -> None:
    fetch("X_hrsa_health_center_sites",
          "https://data.hrsa.gov/DataDownload/DD_Files/Health_Center_Service_Delivery_and_LookAlike_Sites.csv",
          "Health_Center_Service_Delivery_and_LookAlike_Sites.csv",
          note="HRSA health center (FQHC and look-alike) service delivery sites, national", force=ARGS.force)


def src_X_facilities() -> None:
    key = "X_chhs_facility_locations"
    pkg = ckan_package(key, "healthcare-facility-locations")
    if not pkg:
        return
    for r in pkg["resources"]:
        n = r["name"].lower()
        fmt = (r.get("format") or "").upper()
        if fmt == "CSV" and n.startswith("licensed and certified healthcare facility locations"):
            fetch_resource(key, r)
        elif "data dictionary" in n and "across time" not in n and fmt in ("XLSX", "XLS", "CSV"):
            fetch_resource(key, r)
        elif "lookup table" in n and fmt in ("XLSX", "XLS"):
            fetch_resource(key, r)


def src_X_ruca() -> None:
    key = "X_usda_ruca_zip"
    page = "https://www.ers.usda.gov/data-products/rural-urban-commuting-area-codes"
    try:
        html = get_text(page)
    except Exception as e:  # noqa: BLE001
        record(key, page, status="failed", blocker=f"landing page: {e}")
        return
    m = re.search(r'href="([^"]*2020-rural-urban-commuting-area-codes-zip-codes\.csv[^"]*)"', html)
    if not m:
        record(key, page, status="failed", blocker="2020 ZIP-code RUCA CSV link not found on landing page")
        return
    url = urljoin(page, m.group(1))
    fetch(key, url, "2020-rural-urban-commuting-area-codes-zip-codes.csv",
          note="USDA ERS 2020 RUCA codes by ZIP code (postal ZIP, derived from tract RUCA)", force=ARGS.force)


def src_X_nppes() -> None:
    """Feasibility only. Never downloads the multi-GB bulk file; no provider records are saved."""
    key = "X_nppes_feasibility"
    landing = "https://download.cms.gov/nppes/NPI_Files.html"
    note = ""
    try:
        txt = SESSION.get(landing, timeout=TIMEOUT).text.lower()
        if "down for maint" in txt:
            note = "landing page shows 'site will be down for maintenance until further notice'"
        zips = re.findall(r'href="([^"]*nppes_data_dissemination[^"]*\.zip)"', txt)
    except Exception as e:  # noqa: BLE001
        zips, note = [], f"landing page error: {e}"
    size = ""
    url = landing
    if zips:
        url = urljoin(landing, zips[0])
        try:
            r = SESSION.head(url, timeout=TIMEOUT, allow_redirects=True)
            size = r.headers.get("content-length", "")
        except Exception:  # noqa: BLE001
            pass
        record(key, url, bytes=size, status="feasible_not_downloaded",
               note="HEAD only; multi-GB file deliberately not downloaded in Phase 0. " + note)
    else:
        record(key, landing, status="bulk_file_not_confirmed",
               blocker="No NPPES bulk zip link was listed on the CMS download page. " + note +
                       " Guessed monthly file names returned HTTP 404.",
               note="Not downloaded either way.")
    # The per-query NPI Registry API (not bulk) - status check only, response discarded.
    api = "https://npiregistry.cms.hhs.gov/api/?version=2.1&postal_code=92501&limit=1"
    try:
        r = SESSION.get(api, timeout=TIMEOUT)
        ok = r.status_code == 200 and "result_count" in r.text[:200]
        record(key + "_registry_api", api.split("?")[0], status="feasible_not_downloaded" if ok else "failed",
               blocker="" if ok else f"HTTP {r.status_code}",
               note="NPI Registry API answers (keyless, per-query, rate-limited, not a bulk source); response discarded")
    except Exception as e:  # noqa: BLE001
        record(key + "_registry_api", api.split("?")[0], status="failed", blocker=str(e))


STEPS = {
    "A": src_A, "B": src_B, "C": src_C, "D": src_D, "E": src_E, "F": src_F, "G": src_G, "H": src_H,
    "X_census": src_X_census, "X_acs": src_X_acs, "X_places": src_X_places,
    "X_hrsa_sites": src_X_hrsa_sites, "X_facilities": src_X_facilities, "X_ruca": src_X_ruca,
    "X_nppes": src_X_nppes,
}

ARGS: argparse.Namespace


def main() -> int:
    global ARGS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", choices=list(STEPS), help="run only these steps")
    ap.add_argument("--force", action="store_true", help="re-download even if cached; the fresh copy is saved beside the original (raw files are never overwritten)")
    ARGS = ap.parse_args()
    load_manifest()
    for name, fn in STEPS.items():
        if ARGS.only and name not in ARGS.only:
            continue
        log(f"=== {name}")
        try:
            fn()
        except SystemExit:
            raise
        except Exception as e:  # noqa: BLE001  one source failing must not stop the rest
            record(f"{name}__step_error", "(script)", status="failed", blocker=f"{type(e).__name__}: {e}")
            log(f"{name}: step error {e}")
    save_manifest()
    bad = [r for r in MANIFEST_ROWS.values() if r["status"] in ("failed",)]
    log(f"done: {len(MANIFEST_ROWS)} manifest rows, {len(bad)} failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
