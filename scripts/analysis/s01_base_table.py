"""Step 1: geography + base table (one row per IE-touching ZCTA) + reconciliation against county totals (B).

Outputs
  data/processed/zcta_geo_region.parquet     all ZCTAs within BUFFER_KM of an IE ZCTA (points, area, pop-weighted point)
  data/processed/zcta_demand_region.parquet  Medi-Cal eligibles 2026-09 for every CA ZCTA in the region (catchment demand)
  data/processed/base_table.parquet          169 IE-touching ZCTAs, eligibles x 3 months, county rule, flags
  data/processed/zip_no_zcta.parquet         ZIPs in A without a ZCTA
  data/processed/zcta_geometry_region.gpkg   polygons for region ZCTAs (maps, contiguity)
  outputs/tables/s01_*.csv, data/quality section 'base_table'
[COMPUTED: scripts/analysis/s01_base_table.py]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import zipfile, io
import numpy as np, pandas as pd, geopandas as gpd
from config import *

con = duck()
A = RAW / "A_zip_eligibles_2020_recent" / "oct2026_productionsecondsheet_2020_recent.csv"
con.execute(f"create view A as select * from read_csv('{A}', all_varchar=true, header=true)")

# ---------------------------------------------------------------- A: ZIP x month, sex-resolved
a = con.execute(f"""
 select trim("Zip Code") as zip, "Month of Eligibility" as month, "Sex" as sex,
        {num('"Total Eligibles"')} as n, "Annotation Code" as ann, "Status" as status
 from A where "Month of Eligibility" in ('2026-09','2026-08','2025-09','2026-10')
""").df()
a["n"] = a.n.astype("float64")
a_tot = a[a.sex == "Total"].copy()
statewide = a_tot[a_tot.zip == "STATEWIDE"].set_index("month").n.to_dict()
invalid_zip = a_tot[a_tot.zip == "."].set_index("month").n.to_dict()
a_zip = a_tot[a_tot.zip.str.fullmatch(r"\d{5}")].copy()

# ---------------------------------------------------------------- geography
gaz = pd.read_csv(zipfile.ZipFile(RAW / "X_zcta_gazetteer/2020_Gaz_zcta_national.zip").open("2020_Gaz_zcta_national.txt"),
                  sep="\t", dtype={"GEOID": str})
gaz.columns = [c.strip() for c in gaz.columns]
gaz = gaz.rename(columns={"GEOID": "zcta", "INTPTLAT": "int_lat", "INTPTLONG": "int_lon", "ALAND": "aland_m2"})[
    ["zcta", "aland_m2", "int_lat", "int_lon"]]

rel_cty = pd.read_csv(RAW / "H_census_zcta_county/tab20_zcta520_county20_natl.txt", sep="|", dtype=str, encoding="utf-8-sig")
rel_cty = rel_cty[rel_cty.GEOID_ZCTA5_20.notna() & (rel_cty.GEOID_ZCTA5_20 != "")].copy()
rel_cty["land"] = rel_cty.AREALAND_PART.astype(float)
rel_cty = rel_cty.rename(columns={"GEOID_ZCTA5_20": "zcta", "GEOID_COUNTY_20": "county_fips"})[["zcta", "county_fips", "land"]]
ie_touch = sorted(rel_cty[rel_cty.county_fips.isin(IE_FIPS) & (rel_cty.land > 0)].zcta.unique())
print("IE-touching ZCTAs:", len(ie_touch))

# land-area majority county, state-out share
tot_land = rel_cty.groupby("zcta").land.sum().rename("land_total")
idx = rel_cty.groupby("zcta").land.idxmax()
land_major = rel_cty.loc[idx].set_index("zcta")[["county_fips", "land"]].rename(columns={"county_fips": "land_major_fips", "land": "land_major"})
land_major = land_major.join(tot_land)
land_major["land_major_share"] = land_major.land_major / land_major.land_total
rel_cty["is_ca"] = rel_cty.county_fips.str.startswith("06")
share_out_ca = (rel_cty[~rel_cty.is_ca].groupby("zcta").land.sum() / tot_land).rename("land_share_outside_ca").fillna(0)
land_ie = rel_cty[rel_cty.county_fips.isin(IE_FIPS)].groupby("zcta").land.sum().rename("land_ie")
land_by_cty = rel_cty.pivot_table(index="zcta", columns="county_fips", values="land", aggfunc="sum").fillna(0)

# tract -> ZCTA: pop-weighted county shares and pop-weighted points (approximation: uniform density in tract)
rt = pd.read_csv(RAW / "X_tract_zcta/tab20_zcta520_tract20_natl.txt", sep="|", dtype=str, encoding="utf-8-sig")
rt = rt[rt.GEOID_ZCTA5_20.notna() & (rt.GEOID_ZCTA5_20 != "") & rt.GEOID_TRACT_20.str.startswith("06")].copy()
rt["part"] = rt.AREALAND_PART.astype(float)
rt["tract_land"] = rt.AREALAND_TRACT_20.astype(float)
rt = rt.rename(columns={"GEOID_ZCTA5_20": "zcta", "GEOID_TRACT_20": "tract"})[["zcta", "tract", "part", "tract_land"]]
cp = pd.read_csv(RAW / "X_cenpop2020_tract/CenPop2020_Mean_TR06.txt", dtype={"STATEFP": str, "COUNTYFP": str, "TRACTCE": str},
                 encoding="utf-8-sig")
cp["tract"] = cp.STATEFP + cp.COUNTYFP + cp.TRACTCE
cp["county_fips"] = cp.STATEFP + cp.COUNTYFP
cp = cp.rename(columns={"POPULATION": "tract_pop", "LATITUDE": "t_lat", "LONGITUDE": "t_lon"})[["tract", "county_fips", "tract_pop", "t_lat", "t_lon"]]
rt = rt.merge(cp, on="tract", how="left")
rt["tract_pop"] = rt.tract_pop.fillna(0)
# a tract entirely water/zero land: part/tract_land -> NaN
rt["w"] = np.where(rt.tract_land > 0, rt.part / rt.tract_land, 0.0).clip(0, 1)
rt["pop_piece"] = rt.tract_pop * rt.w
popz = rt.groupby("zcta").pop_piece.sum().rename("pop_est_ca")
pc = rt.assign(lat_w=rt.t_lat * rt.pop_piece, lon_w=rt.t_lon * rt.pop_piece).groupby("zcta")[["lat_w", "lon_w", "pop_piece"]].sum()
pc["pw_lat"] = pc.lat_w / pc.pop_piece.replace(0, np.nan)
pc["pw_lon"] = pc.lon_w / pc.pop_piece.replace(0, np.nan)
pop_by_cty = rt.pivot_table(index="zcta", columns="county_fips", values="pop_piece", aggfunc="sum").fillna(0)

geo = gaz.set_index("zcta").join(pc[["pw_lat", "pw_lon"]]).join(popz).join(land_major).join(share_out_ca).reset_index()
geo["pw_lat"] = geo.pw_lat.fillna(geo.int_lat)
geo["pw_lon"] = geo.pw_lon.fillna(geo.int_lon)
geo["pw_is_fallback"] = geo.pw_lat.eq(geo.int_lat) & geo.pw_lon.eq(geo.int_lon)

# ---------------------------------------------------------------- region (BUFFER_KM of any IE-touching internal point)
from pyproj import Transformer
tr = Transformer.from_crs(4326, 3310, always_xy=True)  # California Albers (metres)
geo["x"], geo["y"] = tr.transform(geo.pw_lon.values, geo.pw_lat.values)
ie_pts = geo[geo.zcta.isin(ie_touch)][["x", "y"]].values
from scipy.spatial import cKDTree
tree = cKDTree(ie_pts)
geo["dist_to_ie_km"] = tree.query(geo[["x", "y"]].values)[0] / 1000.0
region = geo[(geo.dist_to_ie_km <= BUFFER_KM)].copy()
print("region ZCTAs within", BUFFER_KM, "km:", len(region))

# ---------------------------------------------------------------- county assignment for IE-touching ZCTAs
def assign(z):
    row = {"zcta": z}
    pops = pop_by_cty.loc[z] if z in pop_by_cty.index else None
    lands = land_by_cty.loc[z]
    row["land_major_fips"] = lands.idxmax()
    row["land_major_share"] = lands.max() / lands.sum()
    if pops is not None and pops.sum() > 0:
        pshare = pops / pops.sum()
        top = pshare.sort_values(ascending=False)
        row["pop_major_fips"] = top.index[0]
        row["pop_major_share"] = float(top.iloc[0])
        row["pop_share_riverside"] = float(pshare.get(RIV, 0))
        row["pop_share_sanbern"] = float(pshare.get(SB, 0))
        row["pop_share_other_ca"] = float(1 - pshare.get(RIV, 0) - pshare.get(SB, 0))
        row["second_fips"] = top.index[1] if len(top) > 1 and top.iloc[1] > 0 else None
        row["second_share"] = float(top.iloc[1]) if len(top) > 1 else 0.0
    else:
        row.update(pop_major_fips=None, pop_major_share=np.nan, pop_share_riverside=np.nan, pop_share_sanbern=np.nan,
                   pop_share_other_ca=np.nan, second_fips=None, second_share=np.nan)
    return row

assn = pd.DataFrame([assign(z) for z in ie_touch])
# Rule: county = county holding the largest ESTIMATED POPULATION share (Census 2020 tract populations x tract-ZCTA land overlap).
# Fallback to land-area majority if no tract population. Split flag: second county >= 10% of ZCTA population (or >=10% of land if no pop).
assn["county_fips"] = assn.pop_major_fips.fillna(assn.land_major_fips)
assn["county"] = assn.county_fips.map(COUNTY_NAMES).fillna(assn.county_fips)
assn["county_rule_differs_from_land"] = assn.county_fips != assn.land_major_fips
assn["share_outside_assigned_county"] = (1 - assn.pop_major_share).fillna(1 - assn.land_major_share)
assn["is_split_zcta"] = assn.share_outside_assigned_county >= 0.10          # >=10% of ZCTA population (est.) outside its assigned county
assn["is_split_zcta_5pct"] = assn.share_outside_assigned_county >= 0.05
assn["in_ie_study"] = assn.county_fips.isin(IE_FIPS)

# ---------------------------------------------------------------- Medi-Cal eligibles per ZCTA (3 months + Oct)
zcta_set = set(geo.zcta) | set(rel_cty.zcta)        # ZCTAs in the Census relationship file (a few have no polygon / gazetteer point)
pd.DataFrame({'zcta': sorted(zcta_set)}).to_parquet(PROC / 'zcta_universe.parquet', index=False)
no_geom = zcta_set - set(geo.zcta)
piv = {}
for m in ["2026-09", "2026-08", "2025-09", "2026-10"]:
    s = a_zip[a_zip.month == m].set_index("zip")
    piv[m] = s
zip_all = sorted(set(a_zip.zip))
elig = pd.DataFrame(index=zip_all)
for m in ["2026-09", "2026-08", "2025-09", "2026-10"]:
    k = m.replace("-", "_")
    s = piv[m]
    elig[f"elig_{k}"] = s.n.reindex(elig.index)
    elig[f"supp_{k}"] = s.n.reindex(elig.index).isna() & s.ann.reindex(elig.index).notna()
    elig[f"present_{k}"] = elig.index.isin(s.index)
    elig[f"ann_{k}"] = s.ann.reindex(elig.index)
elig.index.name = "zip"
elig = elig.reset_index()
elig["zip_has_zcta"] = elig.zip.isin(zcta_set)

# ---- ZIPs in A without a ZCTA
nz = elig[~elig.zip_has_zcta].copy()
# county hint from E (modal CountyName for ZIP) + CHHS facilities (COUNTY_NAME by ZIP)
E = RAW / "E_ffs_providers" / "medi-cal-ffs-provider-listing_10_26_26.csv"
hint = con.execute(f"""
 select ZIP as zip, CountyName as cname, count(*) n from read_csv('{E}', all_varchar=true, header=true, encoding='latin-1')
 where State='CA' and ZIP is not null and CountyName is not null group by 1,2""").df()
hint = hint.sort_values("n", ascending=False).drop_duplicates("zip").set_index("zip").cname
nz["county_hint_from_E"] = nz.zip.map(hint)
nz["ie_hint"] = nz.county_hint_from_E.isin(["Riverside County", "San Bernardino County"])
nz.to_parquet(PROC / "zip_no_zcta.parquet", index=False)
nz_summary = {
    "statewide_zips_in_A_2026_09": int(elig.present_2026_09.sum()),
    "zips_without_zcta": int((~elig.zip_has_zcta & elig.present_2026_09).sum()),
    "members_without_zcta_statewide_2026_09": int(nz.elig_2026_09.sum()),
    "zips_without_zcta_ie_hint": int(nz.ie_hint.sum()),
    "members_without_zcta_ie_hint_2026_09": int(nz[nz.ie_hint].elig_2026_09.sum()),
    "zips_without_zcta_no_county_hint": int(nz.county_hint_from_E.isna().sum()),
    "members_without_zcta_no_county_hint_2026_09": int(nz[nz.county_hint_from_E.isna()].elig_2026_09.sum()),
    "invalid_or_outofstate_zip_dot_members_2026_09": int(invalid_zip.get("2026-09", 0)),
    "statewide_total_A_2026_09": int(statewide.get("2026-09", 0)),
}

# ---------------------------------------------------------------- base table (IE-touching ZCTAs)
base = assn.merge(geo[["zcta", "aland_m2", "int_lat", "int_lon", "pw_lat", "pw_lon", "pw_is_fallback", "pop_est_ca", "land_share_outside_ca"]], on="zcta", how="left")
e2 = elig.rename(columns={"zip": "zip_in_A"})
base = base.merge(e2, left_on="zcta", right_on="zip_in_A", how="left")
base["zip"] = base.zip_in_A                        # postal ZIP with the same 5 digits found in A (NaN if absent)
base["zcta"] = base.zcta.astype(str)
base["in_A"] = base.zip_in_A.notna()
base["has_geometry"] = base.pw_lat.notna()
base["elig_primary"] = base.elig_2026_09
base["is_suppressed"] = base.supp_2026_09.fillna(False) | (base.elig_2026_09.isna())
# bounds: suppressed small number => 1..10 per DHCS cell suppression (code 1). Midpoint 5.5 used only where a number is unavoidable.
base["elig_primary_lo"] = base.elig_primary.fillna(1)
base["elig_primary_hi"] = base.elig_primary.fillna(10)
base["elig_primary_imputed"] = base.elig_primary.fillna(5.5)
base["pop_acs_total"] = np.nan   # filled in s02/s05 context join (ACS)
base["min_base_ok"] = base.elig_primary >= 500
cols_first = ["zcta", "zip", "in_A", "county", "county_fips", "in_ie_study", "is_split_zcta", "elig_primary", "is_suppressed"]
base = base[cols_first + [c for c in base.columns if c not in cols_first and c != "zip_in_A"]]
assert base.zcta.is_unique
base.to_parquet(PROC / "base_table.parquet", index=False)

# ---------------------------------------------------------------- demand file for the catchment (all CA ZCTAs in the region)
dem = region[["zcta", "pw_lat", "pw_lon", "x", "y", "dist_to_ie_km", "int_lat", "int_lon", "pop_est_ca", "land_share_outside_ca"]].merge(
    elig[["zip", "elig_2026_09", "supp_2026_09", "present_2026_09"]].rename(columns={"zip": "zcta"}), on="zcta", how="left")
# county of every region ZCTA (population major, CA tracts only; else land-major)
pmaj = pop_by_cty.idxmax(axis=1).rename("pop_major_fips")
dem = dem.merge(pmaj, left_on="zcta", right_index=True, how="left").merge(land_major[["land_major_fips"]], left_on="zcta", right_index=True, how="left")
dem["county_fips"] = dem.pop_major_fips.fillna(dem.land_major_fips)
dem["county"] = dem.county_fips.map(COUNTY_NAMES).fillna(dem.county_fips)
dem["is_ca_demand"] = dem.county_fips.fillna("").str.startswith("06") & dem.present_2026_09.fillna(False)
dem["elig_2026_09_imputed"] = np.where(dem.is_ca_demand, dem.elig_2026_09.fillna(5.5), 0.0)
dem.to_parquet(PROC / "zcta_demand_region.parquet", index=False)
region.to_parquet(PROC / "zcta_geo_region.parquet", index=False)
geo.to_parquet(PROC / "zcta_points_all.parquet", index=False)

# polygons for region ZCTAs
gz = gpd.read_file(f"zip://{RAW / 'X_tiger_zcta_2020' / 'cb_2020_us_zcta520_500k.zip'}")
gz = gz.rename(columns={"ZCTA5CE20": "zcta"})
zcta_universe = set(gz.zcta)
gz[gz.zcta.isin(set(region.zcta))][["zcta", "geometry"]].to_file(PROC / "zcta_geometry_region.gpkg", driver="GPKG")
tiger_universe_n = len(zcta_universe)

# ---------------------------------------------------------------- reconciliation vs B county totals
B2 = RAW / "B_delivery_plan" / "t2_eligibility_by_delivery_system_plan_201001_oct2026.csv"
b = con.execute(f"""select "Month of Eligibility" as month, County as county, "Health Delivery System" as sys, "Health Plan" as plan,
     {num('"Total Eligibles"')} as n, "Annotation Code" as ann, Status as status
     from read_csv('{B2}', all_varchar=true, header=true)""").df()
b["n"] = b.n.astype("float64")
b_cty = b[b.month.isin(ALL_MONTHS + ["2026-10"])].groupby(["month", "county"]).n.sum(min_count=1).unstack("month")
rec_rows = []
for m in ALL_MONTHS:
    k = m.replace("-", "_")
    for cty, fips, bname in [("Riverside", RIV, "Riverside"), ("San Bernardino", SB, "San Bernardino")]:
        B_total = float(b_cty.loc[bname, m])
        # (1) naive: sum of A over ZCTAs assigned to the county by population-majority rule (all CA ZCTAs, not only IE-touching ones)
        sub = dem if False else None
        a_m = a_zip[a_zip.month == m].set_index("zip").n
        # county major for ALL ZCTAs
        allmaj = pop_by_cty.idxmax(axis=1)
        allmaj = allmaj.reindex(sorted(zcta_set)).fillna(land_major.land_major_fips.reindex(sorted(zcta_set)))
        z_in = [z for z in a_m.index if allmaj.get(z) == fips]
        naive = float(a_m.reindex(z_in).sum())
        # (2) IE-touching ZCTAs, full count (the guide's route): any ZCTA touching either IE county
        touch = float(a_m.reindex([z for z in ie_touch]).sum())
        # (3) proportional allocation by estimated population share (uniform-share on ALL eligibles; not status-specific)
        alloc = 0.0
        for z in a_m.index:
            if z in pop_by_cty.index:
                tp = pop_by_cty.loc[z].sum()
                if tp > 0 and pop_by_cty.loc[z].get(fips, 0) > 0:
                    alloc += np.nan_to_num(a_m.get(z, 0)) * pop_by_cty.loc[z][fips] / tp
        # land-area allocation for comparison
        alloc_land = 0.0
        for z in a_m.index:
            if z in land_by_cty.index and land_by_cty.loc[z].sum() > 0 and land_by_cty.loc[z].get(fips, 0) > 0:
                alloc_land += np.nan_to_num(a_m.get(z, 0)) * land_by_cty.loc[z][fips] / land_by_cty.loc[z].sum()
        rec_rows.append(dict(month=m, county=cty, B_total=B_total, A_majority_rule=naive, A_pop_share_alloc=alloc,
                             A_land_share_alloc=alloc_land, A_all_ie_touching_zctas_both_counties=touch))
rec = pd.DataFrame(rec_rows)
for c in ["A_majority_rule", "A_pop_share_alloc", "A_land_share_alloc"]:
    rec[c + "_pct_vs_B"] = 100 * (rec[c] / rec.B_total - 1)
rec.to_csv(TAB / "s01_reconciliation_A_vs_B.csv", index=False)
# the guide-route overshoot (both counties together)
touch_pct = {}
for m in ALL_MONTHS:
    t = rec[rec.month == m]
    touch_pct[m] = dict(A_ie_touching_zctas=float(t.A_all_ie_touching_zctas_both_counties.iloc[0]),
                        B_both_counties=float(t.B_total.sum()),
                        pct_over=float(100 * (t.A_all_ie_touching_zctas_both_counties.iloc[0] / t.B_total.sum() - 1)))

# decomposition of the ~3% gap for 2026-09 (both counties): sum over IE-touching ZCTAs of eligibles by whether ZCTA is wholly/partly in IE
a09 = a_zip[a_zip.month == "2026-09"].set_index("zip").n
dec = base.assign(elig=base.elig_primary.fillna(0))
dec["pop_share_ie"] = dec.pop_share_riverside.fillna(0) + dec.pop_share_sanbern.fillna(0)
dec["elig_in_ie_est"] = dec.elig * dec.pop_share_ie
decomp = dict(
    A_ie_touching_total=float(dec.elig.sum()),
    est_members_outside_ie_inside_touching_zctas=float((dec.elig - dec.elig_in_ie_est).sum()),
    est_ie_members_in_touching_zctas=float(dec.elig_in_ie_est.sum()),
    B_both_counties=float(rec[rec.month == "2026-09"].B_total.sum()),
)
decomp["residual_B_minus_est_ie_members"] = decomp["B_both_counties"] - decomp["est_ie_members_in_touching_zctas"]
decomp["note"] = ("A-minus-B overshoot is mostly split ZCTAs that include residents of other counties/states; B is by county of residence. "
                  "Residual includes ZIPs without ZCTA, invalid ZIPs ('.'), suppressed cells, and error in the area-uniform population assumption.")

# ---------------------------------------------------------------- summaries and checks
inie = base[base.in_ie_study]
sumtab = pd.DataFrame({
    "n_zcta_ie_touching": [len(base)], "n_zcta_assigned_ie": [len(inie)],
    "n_split_zcta_10pct": [int(base.is_split_zcta.sum())], "n_split_zcta_5pct": [int(base.is_split_zcta_5pct.sum())], "n_suppressed_primary": [int(base.is_suppressed.sum())],
    "n_not_in_A": [int((~base.in_A).sum())], "n_lt500_eligibles": [int((base.elig_primary < 500).sum())],
    "n_rule_differs_from_land": [int(base.county_rule_differs_from_land.sum())],
    "elig_sum_assigned_ie": [float(inie.elig_primary.sum())], "elig_sum_all_touching": [float(base.elig_primary.sum())]})
sumtab.to_csv(TAB / "s01_base_table_summary.csv", index=False)
base[["zcta", "zip", "county", "is_split_zcta", "pop_share_riverside", "pop_share_sanbern", "pop_share_other_ca", "land_major_fips", "pop_major_fips",
      "elig_2026_09", "elig_2026_08", "elig_2025_09", "is_suppressed"]].to_csv(TAB / "s01_county_assignment_and_eligibles.csv", index=False)
update_checks("base_table", dict(
    ie_touching_zctas=len(base), ie_touching_expected=169, zctas_in_A_2026_09=int(base.in_A.sum()),
    zcta_missing_from_A=base[~base.in_A].zcta.tolist(), zcta_key_unique=bool(base.zcta.is_unique),
    split_zctas_10pct=int(base.is_split_zcta.sum()), split_zctas_5pct=int(base.is_split_zcta_5pct.sum()), assigned_riverside=int((base.county_fips == RIV).sum()),
    assigned_sanbernardino=int((base.county_fips == SB).sum()), assigned_other=int((~base.in_ie_study).sum()),
    suppressed_primary=int(base.is_suppressed.sum()), suppressed_zctas=base[base.is_suppressed].zcta.tolist(),
    count_rule_differs_from_land=int(base.county_rule_differs_from_land.sum()),
    region_zctas=len(region), tiger_zcta_universe=tiger_universe_n, buffer_km=BUFFER_KM,
    zip_no_zcta=nz_summary, ie_touching_zcta_without_polygon=base[~base.has_geometry].zcta.tolist(),
    ie_touching_zcta_without_polygon_eligibles_2026_09=float(base[~base.has_geometry].elig_primary.sum()), reconciliation=rec.to_dict("records"), touching_overshoot=touch_pct, gap_decomposition_2026_09=decomp,
    a_statewide_total_by_month={k: int(v) for k, v in statewide.items()},
    a_sum_valid_zip_by_month={m: int(a_zip[a_zip.month == m].n.sum()) for m in ["2026-09", "2026-08", "2025-09", "2026-10"]},
    a_invalid_zip_dot_by_month={k: int(v) for k, v in invalid_zip.items()},
))
print(sumtab.T); print(rec.round(1).to_string()); print(touch_pct); print(decomp); print(nz_summary)
