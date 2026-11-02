"""Step 2: classify every FFS provider record (source E, statewide) and build supply by category x definition.

Definitions (per supply group g):
  a  BROAD    every enrolled record whose type/specialty/taxonomy/ANC maps to g (all Provider_Source, group rows included,
              no dedupe; for primary care also physicians with unknown specialty = an upper bound)
  b  DEDUPED  unique NPI-ZIP, individual practitioners only, Provider_Source 1 or 2, classifiable, group rows removed
  c  STRICT   b, Provider_Source 1 only, hospital-based specialties removed (radiology, anesthesiology, pathology, emergency,
              nuclear medicine, radiation therapy, hospitalists), and records that self-report NOT taking new FFS patients
              (Medicaid_Patients N or M) removed
  d  BILLABLE c restricted to records that can plausibly be paid at their site: the record itself is an 'FFS Billing Provider', or a
              billing-provider record exists at the same street address + ZIP (non-billing individuals bill through a group)
  e  ADDRCAP  b with each street address counted at most ADDR_CAP (25) records per supply group (hospital-campus / large-building check)
Dental (source F, Oct 2025): a all rows; b unique rendering NPI-ZIP (R, RC); c b without hygienists / faculty / blank specialty;
  d c at private offices only (R, not safety-net-clinic rendering).
Outputs: data/processed/provider_classified.parquet (no names/phones/addresses), supply_by_zcta.parquet,
  supply_points_region.parquet, outputs/tables/s02_*.csv
[COMPUTED: scripts/analysis/s02_supply.py]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd, geopandas as gpd, hashlib
from config import *

con = duck()
E = RAW / "E_ffs_providers" / "medi-cal-ffs-provider-listing_10_26_26.csv"
df = con.execute(f"""
 select row_number() over () as row_id, NPI as npi, Provider_Number as provider_number, NPI_Type as npi_type,
   FI_Provider_Type_CD as ptype, FI_Provider_Type as ptype_desc, FI_Provider_Specialty_CD as spec, FI_Provider_Specialty as spec_desc,
   Provider_Taxonomy as tax, ANC_Provider_Type as anc, Provider_Source as source, Billing_Provider as billing,
   Medicaid_Patients as mcal_flag, Telehealth_Services as telehealth, State as state, ZIP as zip, upper(trim(coalesce(Address,''))) as addr, upper(trim(coalesce(Address2,''))) as addr2,
   County as county_label, CountyName as county_name, try_cast(Latitude as double) as lat, try_cast(Longitude as double) as lon,
   In_Out_State as in_out_state, Enroll_Status_Eff_DT as eff_dt
 from read_csv('{E}', all_varchar=true, header=true, encoding='latin-1')""").df()
n_total_rows = len(df)
for c in ["ptype", "spec", "tax", "anc", "source", "billing", "mcal_flag", "zip", "county_name", "county_label", "state"]:
    df[c] = df[c].astype("object").str.strip()
df["spec"] = df.spec.where(~df.spec.isin(["", "-", "N/A", "n/a"]), np.nan)
df["spec_norm"] = df.spec.str.zfill(2)
df["tax"] = df.tax.where(df.tax.str.fullmatch(r"[0-9A-Z]{9}[A-Z0-9]", na=False), np.nan)
df["zip"] = df.zip.where(df.zip.str.fullmatch(r"\d{5}", na=False), np.nan)
df["is_ca"] = df.state.eq("CA")
df["in_ie"] = df.is_ca & (df.county_label.isin(["Riverside", "San Bernardino"]) | df.county_name.isin(["Riverside County", "San Bernardino County"]))
df["ie_county"] = np.where(df.county_name.eq("Riverside County") | (df.county_label.eq("Riverside") & df.county_name.isna()), "Riverside",
                    np.where(df.county_name.eq("San Bernardino County") | (df.county_label.eq("San Bernardino") & df.county_name.isna()), "San Bernardino", None))
df["addr_key"] = (df.addr.fillna("") + "|" + df.addr2.fillna("") + "|" + df.zip.fillna("")).map(lambda s: hashlib.md5(s.encode()).hexdigest()[:12])
df["npi_key"] = df.npi.where(df.npi.notna() & ~df.npi.isin(["", "0", "0000000000"]), "PN" + df.provider_number.astype("object"))

# ------------------------------------------------------------------ classification (spec code > taxonomy > ANC)
SPEC_PC = {"08", "41", "40", "01", "38"}
SPEC_OBGYN = {"16", "15", "09"}
SPEC_CARD = {"06", "35"}
SPEC_ENDO = {"67"}
SPEC_PSY = {"36", "26", "27"}
SPEC_HOSP = {"30", "31", "05", "22", "21", "90", "66", "42", "32"}
SPEC_UNINFORMATIVE = {"47", "44", "39", "70", "49", "60", "92", "91", "11", "19", "12"}   # Misc, public health, preventive, mixed clinic, unknown...
SPEC_OTHER = set("02 03 04 07 10 13 14 17 18 20 23 24 25 28 29 33 34 43 45 46 68 77 78 79 83 84 85 89".split())

def tax_class(t):
    if not isinstance(t, str):
        return None
    if t == "390200000X": return "unclass"
    if t in ("207Q00000X", "207QA0000X", "207QG0300X", "208D00000X", "208000000X", "207R00000X", "207RG0300X") or t.startswith("207QA") or t.startswith("207QH") :
        return "pc"
    if t.startswith("207Q") or t.startswith("208D"): return "pc"
    if t.startswith("207V"): return "obgyn"
    if t in ("207RC0000X", "207RI0011X", "2080P0202X") or t.startswith("207RC"): return "cardiology"
    if t == "207RE0101X": return "endocrinology"
    if t.startswith("2084P"): return "psychiatrist"
    if t.startswith("2085") or t.startswith("207L") or t.startswith("207P") or t.startswith("207Z") or t.startswith("207U") or t.startswith("208M"): return "hospital"
    if t.startswith("207") or t.startswith("208") or t.startswith("2086"): return "other_specialist"
    return None

ANC_MAP = {"Adult Primary Care": "pc", "Pediatric Primary Care": "pc", "Obstetrics & Gynecology": "obgyn", "Psychiatry": "psychiatrist",
           "Cardiology/Interventional Cardiology": "cardiology", "Mammography/MRI Provider": "hospital",
           "General Surgery": "other_specialist", "Orthopedic Surgery": "other_specialist", "Neurology": "other_specialist",
           "Gastroenterology": "other_specialist", "Ophthalmology": "other_specialist", "Dermatology": "other_specialist",
           "ENT/Otolaryngology": "other_specialist", "Pulmonology": "other_specialist", "Oncology": "other_specialist",
           "HIV/AIDS/Infectious Disease": "other_specialist", "Physical Medicine and Rehabilitation": "other_specialist"}

def spec_class(c):
    if not isinstance(c, str): return None
    if c in SPEC_PC: return "pc"
    if c in SPEC_OBGYN: return "obgyn"
    if c in SPEC_CARD: return "cardiology"
    if c in SPEC_ENDO: return "endocrinology"
    if c in SPEC_PSY: return "psychiatrist"
    if c in SPEC_HOSP: return "hospital"
    if c in SPEC_OTHER: return "other_specialist"
    if c in SPEC_UNINFORMATIVE: return "uninformative"
    return None

PHYS_TYPES = {"026", "022"}                 # physicians (individual), physician groups
INDIV_TYPES = {"026", "007", "005", "082", "077", "070", "031", "103", "018", "027", "020", "025", "019", "037", "003", "006", "032", "067", "099", "086", "087"}
GROUP_TYPES = {"022", "010", "078", "071", "104", "023", "062"}
CLINIC_FQHC = {"035"}
CLINIC_OTHER = {"041", "045", "048", "096", "075"}
MH_NONPHYS = {"077", "070", "031", "103"}
MH_GROUP = {"078", "071", "104"}
NP_TYPES = {"007", "010"}
MIDWIFE = {"005", "082"}

df["spec_cls"] = df.spec_norm.map(spec_class)
df["tax_cls"] = df.tax.map(tax_class)
df["anc_cls"] = df.anc.map(ANC_MAP)
is_phys = df.ptype.isin(PHYS_TYPES)
phys_cls = df.spec_cls.copy()
basis = pd.Series(np.where(df.spec_cls.notna(), "specialty_code", None), index=df.index, dtype="object")
need = is_phys & (df.spec_cls.isna() | df.spec_cls.eq("uninformative"))
use_tax = need & df.tax_cls.notna() & ~df.tax_cls.eq("unclass")
phys_cls = phys_cls.where(~use_tax, df.tax_cls); basis = basis.where(~use_tax, "taxonomy")
need2 = is_phys & (phys_cls.isna() | phys_cls.eq("uninformative")) & df.anc_cls.notna()
phys_cls = phys_cls.where(~need2, df.anc_cls); basis = basis.where(~need2, "anc_type")
df["phys_cls"] = np.where(is_phys, phys_cls, None)
df["class_basis"] = np.where(is_phys, basis, None)
df.loc[is_phys & df.phys_cls.isna(), "phys_cls"] = "unknown_specialty"
df.loc[is_phys & df.phys_cls.eq("uninformative"), "phys_cls"] = "unknown_specialty"
df["class_basis"] = df.class_basis.where(df.phys_cls.ne("unknown_specialty") | ~is_phys, "none")

# supply-group boolean columns -----------------------------------------------------------
g = pd.DataFrame(index=df.index)
g["pcp_md"] = is_phys & df.phys_cls.eq("pc")
g["np"] = df.ptype.isin(NP_TYPES)
g["clinic_fqhc"] = df.ptype.isin(CLINIC_FQHC)
g["clinic_other"] = df.ptype.isin(CLINIC_OTHER)
g["mh_nonphys"] = df.ptype.isin(MH_NONPHYS | MH_GROUP)
g["psychiatrist"] = is_phys & df.phys_cls.eq("psychiatrist")
g["cardiology"] = is_phys & df.phys_cls.eq("cardiology")
g["obgyn"] = (is_phys & df.phys_cls.eq("obgyn")) | df.ptype.isin(MIDWIFE)
g["endocrinology"] = is_phys & df.phys_cls.eq("endocrinology")
g["specialist_other"] = is_phys & df.phys_cls.eq("other_specialist")
g["hospital_based"] = (is_phys & df.phys_cls.eq("hospital")) | df.ptype.eq("018")
g["phys_unknown_spec"] = is_phys & df.phys_cls.eq("unknown_specialty")
for c in g.columns: df["g_" + c] = g[c]
df["is_individual"] = df.ptype.isin(INDIV_TYPES) & ~df.ptype.isin(GROUP_TYPES)
df["is_group_entity"] = df.ptype.isin(GROUP_TYPES)
df["has_type"] = df.ptype.notna() & ~df.ptype.isin(["N/A", "000"])
df["classifiable"] = g[["pcp_md", "np", "clinic_fqhc", "clinic_other", "mh_nonphys", "psychiatrist", "cardiology", "obgyn", "endocrinology", "specialist_other", "hospital_based"]].any(axis=1)
df["any_group"] = g.any(axis=1)

# ------------------------------------------------------------------ geography of providers: ZIP -> ZCTA, valid coordinates
pts = pd.read_parquet(PROC / "zcta_points_all.parquet")[["zcta", "int_lat", "int_lon", "pw_lat", "pw_lon", "x", "y"]]
zset = set(pd.read_parquet(PROC / 'zcta_universe.parquet').zcta) | set(pts.zcta)
df["zcta_by_zip"] = df.zip.where(df.zip.isin(zset), np.nan)
valid = df.lat.between(31.0, 43.0) & df.lon.between(-125.0, -113.0)       # CA + border strip (NV/AZ/Mexico fringe)
df["coord_valid"] = valid
# distance between provider coordinate and its ZIP's ZCTA internal point (geocode sanity)
from pyproj import Transformer
tr = Transformer.from_crs(4326, 3310, always_xy=True)
x, y = tr.transform(df.lon.fillna(0).values, df.lat.fillna(0).values)
df["x"], df["y"] = x, y
ptmap = pts.set_index("zcta")
zi = df.zcta_by_zip.map(ptmap.x), df.zcta_by_zip.map(ptmap.y)
d_zip = np.sqrt((df.x - zi[0].astype(float)) ** 2 + (df.y - zi[1].astype(float)) ** 2) / 1000
df["dist_coord_to_zip_pt_km"] = d_zip
df["coord_suspect"] = valid & (d_zip > 40)      # geocode >40 km from ZIP's ZCTA point
# location used in catchment: coordinate when valid and not suspect, else ZCTA internal point of ZIP, else none
use_coord = valid & ~df.coord_suspect
loc_x = np.where(use_coord, df.x, zi[0].astype(float)); loc_y = np.where(use_coord, df.y, zi[1].astype(float))
df["loc_x"], df["loc_y"] = loc_x, loc_y
df["loc_source"] = np.where(use_coord, "coordinate", np.where(~np.isnan(loc_x), "zip_zcta_point", "none"))
# rows with no ZCTA for the ZIP but valid coordinates: point-in-polygon on region polygons (IE-relevant ZIPs without ZCTA)
poly = gpd.read_file(PROC / "zcta_geometry_region.gpkg")
need_pip = df.zcta_by_zip.isna() & valid & df.is_ca
if need_pip.any():
    g_pts = gpd.GeoDataFrame(df.loc[need_pip, ["row_id"]], geometry=gpd.points_from_xy(df.loc[need_pip, "lon"], df.loc[need_pip, "lat"]), crs=4269)
    poly = poly.set_crs(4269, allow_override=True)
    j = gpd.sjoin(g_pts, poly[["zcta", "geometry"]], how="left", predicate="within").drop_duplicates("row_id").set_index("row_id").zcta
    df["zcta_by_pip"] = df.row_id.map(j)
else:
    df["zcta_by_pip"] = np.nan
df["zcta"] = df.zcta_by_zip.fillna(df.zcta_by_pip)

# ------------------------------------------------------------------ weights per row for each (group, definition)
SUPPLY_GROUPS = {
    "pcp_md": ["pcp_md"], "np": ["np"], "pcp": ["pcp_md", "np"],
    "clinic_fqhc": ["clinic_fqhc"], "clinic_all": ["clinic_fqhc", "clinic_other"],
    "mh": ["mh_nonphys", "psychiatrist"], "psychiatrist": ["psychiatrist"], "mh_nonphys": ["mh_nonphys"],
    "cardiology": ["cardiology"], "obgyn": ["obgyn"], "endocrinology": ["endocrinology"],
    "specialist_all": ["cardiology", "obgyn", "endocrinology", "specialist_other", "hospital_based"],
}
ZERO_LABEL = {"a": "broad", "b": "deduped", "c": "strict", "d": "billable_at_site", "e": "address_capped"}
ADDR_CAP = 25
src12 = df.source.isin(["1", "2"]); src1 = df.source.eq("1")
not_na = ~df.mcal_flag.isin(["N", "M"])
billing = df.billing.eq("FFS Billing Provider")
bill_addr = set(df.loc[billing & (df.addr != ""), "addr_key"])
billable_site = billing | df.addr_key.isin(bill_addr)
df["own_npi_biller"] = billing
df["billable_at_site"] = billable_site
is_org_group = {"clinic_fqhc", "clinic_other", "clinic_all"}

def mask_for(gname, d):
    cols = SUPPLY_GROUPS[gname]
    m = g[cols].any(axis=1)
    is_clinic = gname in is_org_group
    if d == "a":
        if gname in ("pcp_md", "pcp"):
            m = m | g["phys_unknown_spec"]              # broad upper bound: physicians whose specialty cannot be seen
        if gname == "np" or gname == "pcp":
            m = m | df.ptype.isin(NP_TYPES)
        return m
    m = m & src12
    if not is_clinic:
        m = m & df.is_individual & ~df.is_group_entity
    if gname == "specialist_all" and d in ("c", "d"):
        m = m & ~g["hospital_based"]
    if d in ("c", "d"):
        m = m & src1 & not_na
    if d == "d":
        m = m & billable_site
    return m

W = pd.DataFrame(index=df.index)
for gname in SUPPLY_GROUPS:
    for d in "abcd":
        m = mask_for(gname, d)
        if d == "a":
            W[f"{gname}__{d}"] = m.astype(float)
        else:
            key = (df.npi_key + "|" + df.zip.fillna("")).where(m)
            first = ~key.duplicated(keep="first") & m
            W[f"{gname}__{d}"] = first.astype(float)

for gname in SUPPLY_GROUPS:                      # definition e: address-capped version of b
    wb = W[f"{gname}__b"]
    nad = wb.groupby(df.addr_key).transform("sum")
    W[f"{gname}__e"] = wb * np.minimum(1.0, ADDR_CAP / nad.where(nad > 0, 1.0))

# ------------------------------------------------------------------ dental (source F)
F = RAW / "F_dental_ffs_providers" / "ffsproviderprofileodp_oct2025.csv"
fd = con.execute(f"""select "Provider NPI" npi, "Provider Type Code" ptype, "Provider Specialty Code Desc" spec_desc, "Provider County Desc" county_label,
  "Billing Provider Zip" zip5, "Billing Provider State" state, try_cast(Latitude as double) lat, try_cast(Longitude as double) lon
  from read_csv('{F}', all_varchar=true, header=true, encoding='utf-8')""").df()
fd["zip"] = fd.zip5.astype("object").str.strip().str[:5]
fd["zip"] = fd.zip.where(fd.zip.str.fullmatch(r"\d{5}", na=False), np.nan)
fd["npi_key"] = fd.npi.astype("object").str.strip()
fd["ptype"] = fd.ptype.astype("object").str.strip()
fd["zcta"] = fd.zip.where(fd.zip.isin(zset), np.nan)
vf = fd.lat.between(31, 43) & fd.lon.between(-125, -113)
xf, yf = tr.transform(fd.lon.fillna(0).values, fd.lat.fillna(0).values)
fd["x"], fd["y"] = xf, yf
zf = fd.zcta.map(ptmap.x).astype(float), fd.zcta.map(ptmap.y).astype(float)
dff = np.sqrt((fd.x - zf[0]) ** 2 + (fd.y - zf[1]) ** 2) / 1000
use_c = vf & ~(dff > 40)
fd["loc_x"] = np.where(use_c, fd.x, zf[0]); fd["loc_y"] = np.where(use_c, fd.y, zf[1])
rend = fd.ptype.isin(["R", "RC"])
nonden = fd.spec_desc.fillna("").str.contains("Hygienist|Faculty|Hygienst", case=False)
blank_spec = fd.spec_desc.isna()
fW = pd.DataFrame(index=fd.index)
fW["dental__a"] = 1.0
mb = rend
kb = (fd.npi_key + "|" + fd.zip.fillna("")).where(mb)
fW["dental__b"] = (~kb.duplicated() & mb).astype(float)
mc = rend & ~nonden & ~blank_spec
kc = (fd.npi_key + "|" + fd.zip.fillna("")).where(mc)
fW["dental__c"] = (~kc.duplicated() & mc).astype(float)
md = mc & fd.ptype.eq("R")
kd = (fd.npi_key + "|" + fd.zip.fillna("")).where(md)
fW["dental__d"] = (~kd.duplicated() & md).astype(float)
fW["dental__e"] = fW["dental__b"]            # no address cap applied to dental (billing addresses only); same as b

# ------------------------------------------------------------------ save classified (privacy: no names/addresses/phones; addr hashed)
keep = ["own_npi_biller", "billable_at_site", "row_id", "npi_key", "npi_type", "ptype", "ptype_desc", "spec", "spec_desc", "tax", "anc", "source", "billing", "mcal_flag", "telehealth", "state",
        "zip", "addr_key", "county_label", "county_name", "in_ie", "ie_county", "lat", "lon", "in_out_state", "zcta", "zcta_by_zip", "zcta_by_pip", "phys_cls", "class_basis",
        "is_individual", "is_group_entity", "has_type", "classifiable", "coord_valid", "coord_suspect", "loc_x", "loc_y", "loc_source", "dist_coord_to_zip_pt_km"]
cls = pd.concat([df[keep + [c for c in df.columns if c.startswith("g_")]], W.add_prefix("w_")], axis=1)
cls.to_parquet(PROC / "provider_classified.parquet", index=False)
fcls = pd.concat([fd[["npi_key", "ptype", "spec_desc", "county_label", "zip", "zcta", "loc_x", "loc_y"]], fW.add_prefix("w_")], axis=1)
fcls.to_parquet(PROC / "dental_classified.parquet", index=False)

# ------------------------------------------------------------------ supply by ZCTA for IE-touching ZCTAs (+ region)
wcols = [c for c in cls.columns if c.startswith("w_")]
sup = cls[cls.zcta.notna()].groupby("zcta")[wcols].sum()
fsup = fcls[fcls.zcta.notna()].groupby("zcta")[[c for c in fcls.columns if c.startswith("w_")]].sum()
sup = sup.join(fsup, how="outer").fillna(0.0)
base = pd.read_parquet(PROC / "base_table.parquet")
reg = pd.read_parquet(PROC / "zcta_geo_region.parquet")
sup_reg = sup.reindex(reg.zcta).fillna(0.0)
sup_reg.index.name = "zcta"
sup_reg.reset_index().to_parquet(PROC / "supply_by_zcta_region.parquet", index=False)
sup_ie = sup.reindex(base.zcta).fillna(0.0); sup_ie.index.name = "zcta"
sup_ie.reset_index().to_parquet(PROC / "supply_by_zcta.parquet", index=False)

# supply points (unique locations) for 2SFCA: weights summed per location. PRIMARY file = California providers only (demand is California Medi-Cal
# residents, so out-of-state providers would face no local competing demand and inflate their provider-to-demand ratio); the "_all" file adds
# NV/AZ/OR border providers for a sensitivity test.
ie_pts = base[["zcta"]].merge(reg[["zcta", "x", "y"]], on="zcta")
from scipy.spatial import cKDTree
tree = cKDTree(ie_pts[["x", "y"]].values)
def near(dfx, km=100.0):
    return tree.query(dfx[["loc_x", "loc_y"]].values)[0] / 1000 <= km
fcols = [c for c in fcls.columns if c.startswith("w_")]
def make_points(ca_only: bool):
    loc = cls[cls.loc_x.notna()]
    floc = fcls[fcls.loc_x.notna()]
    if ca_only:
        loc = loc[loc.state == "CA"]
        floc = floc[fd.loc[floc.index, "state"].astype("object").str.strip().eq("CA")]
    loc = loc[near(loc)].copy(); floc = floc[near(floc)].copy()
    loc["lx"] = loc.loc_x.round(0); loc["ly"] = loc.loc_y.round(0)
    floc["lx"] = floc.loc_x.round(0); floc["ly"] = floc.loc_y.round(0)
    pw = pd.concat([loc.groupby(["lx", "ly"])[wcols].sum(), floc.groupby(["lx", "ly"])[fcols].sum()], axis=1).fillna(0.0)
    return pw[(pw.sum(axis=1) > 0)].reset_index()
make_points(True).to_parquet(PROC / "supply_points_region.parquet", index=False)
make_points(False).to_parquet(PROC / "supply_points_region_with_border_states.parquet", index=False)

# ------------------------------------------------------------------ headline tables
ie = cls[cls.in_ie]
rows = []
for gname in list(SUPPLY_GROUPS):
    for d in "abcde":
        w = ie[f"w_{gname}__{d}"]
        rows.append(dict(group=gname, definition=d, label=ZERO_LABEL[d], records_or_npizip=int(w.sum()),
                         riverside=int(w[ie.ie_county.eq("Riverside")].sum()), san_bernardino=int(w[ie.ie_county.eq("San Bernardino")].sum()),
                         unique_npi=int(ie.loc[w > 0, "npi_key"].nunique())))
for d in "abcde":
    rows.append(dict(group="dental (source F)", definition=d, label=ZERO_LABEL[d], records_or_npizip=int(fW[f"dental__{d}"][fd.zcta.isin(base.zcta)].sum()),
                     riverside=np.nan, san_bernardino=np.nan, unique_npi=int(fd.loc[(fW[f"dental__{d}"] > 0) & fd.zcta.isin(base.zcta), "npi_key"].nunique())))
cnt = pd.DataFrame(rows)
cnt.to_csv(TAB / "s02_supply_counts_by_definition.csv", index=False)
print(cnt.pivot_table(index="group", columns="definition", values="records_or_npizip").round(0).to_string())
# primary-care waterfall (IE, E)
wf = []
m0 = ie.g_pcp_md | ie.g_phys_unknown_spec | ie.g_np
wf.append(("All IE rows", len(ie)))
wf.append(("Physician/NP-type rows that could be primary care (PC specialty, unknown specialty, NP)", int(m0.sum())))
m1 = (ie.g_pcp_md | ie.g_np)
wf.append(("... drop unknown-specialty physicians", int(m1.sum())))
m2 = m1 & ie.source.isin(["1", "2"]); wf.append(("... drop Provider_Source 3", int(m2.sum())))
m3 = m2 & ie.is_individual & ~ie.is_group_entity; wf.append(("... drop group entities", int(m3.sum())))
k = (ie.npi_key + "|" + ie.zip.fillna("")).where(m3); wf.append(("... dedupe NPI-ZIP (definition b)", int((~k.duplicated() & m3).sum())))
wf.append(("definition c (Source 1, not self-reported N/M)", int(ie["w_pcp__c"].sum())))
wf.append(("definition d (billable at site)", int(ie["w_pcp__d"].sum())))
wf.append(("definition e (address cap 25, from b)", round(float(ie["w_pcp__e"].sum()), 1)))
pd.DataFrame(wf, columns=["step", "rows_or_npizip"]).to_csv(TAB / "s02_primary_care_waterfall.csv", index=False)
print(pd.DataFrame(wf))
update_checks("supply_build", dict(
    e_rows_total=int(n_total_rows), ie_rows=int(len(ie)), ie_unique_npi=int(ie.npi_key.nunique()),
    ie_unique_npi_addr_zip=int(ie[["npi_key", "addr_key", "zip"]].drop_duplicates().shape[0]),
    data_report_expected=dict(rows=36470, npi=30520, npi_addr_zip=32529),
    ie_zcta_by_zip_assigned=int(ie.zcta_by_zip.notna().sum()), ie_zcta_by_pip_rescued=int((ie.zcta_by_zip.isna() & ie.zcta_by_pip.notna()).sum()),
    ie_no_zcta=int(ie.zcta.isna().sum()), ie_rows_zip_missing=int(ie.zip.isna().sum()),
    ie_coord_valid=int(ie.coord_valid.sum()), ie_coord_suspect=int(ie.coord_suspect.sum()),
    dental_rows=int(len(fd)), dental_zip_has_zcta=int(fd.zcta.notna().sum()),
))
