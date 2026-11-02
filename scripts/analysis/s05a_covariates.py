"""Step 5a: ZCTA covariates for the correlation work (ACS 2020-2024 5-yr, CDC PLACES 2025, RUCA, HPSA via tract-ZCTA overlap, HRSA FQHC sites).

SENSITIVE LIMIT: no citizenship/nativity/place-of-birth variable is read.  Limited English proficiency (C16001) is used only as an ACCESS-NEED measure
(language barrier to care); it is not a proxy for immigration status and never enters demand allocation.
Output: data/processed/zcta_covariates.parquet   [COMPUTED: scripts/analysis/s05a_covariates.py]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd, geopandas as gpd
from config import *

con = duck()
base = pd.read_parquet(PROC / "base_table.parquet")
zs = list(base.zcta)
ACS = RAW / "X_acs5_zcta"

def acs(table, cells):
    cols = ", ".join([f'try_cast("{table.upper()}_E{c:03d}" as double) as c{c:03d}' for c in cells])
    q = f"""select substr(GEO_ID, 10) as zcta, {cols} from read_csv('{ACS / f"acsdt5y2024-{table}.dat"}', delim='|', header=true, all_varchar=true)
            where GEO_ID like '860Z200US%'"""
    d = con.execute(q).df()
    d = d[d.zcta.isin(zs)].set_index("zcta")
    return d.where(d > -600_000_000)       # sentinel -666666666 etc. -> NaN

pop = acs("b01003", [1]).rename(columns={"c001": "pop_acs"})
b01 = acs("b01001", list(range(1, 50)))
age65 = b01[[f"c{i:03d}" for i in list(range(20, 26)) + list(range(44, 50))]].sum(axis=1)
age_u18 = b01[[f"c{i:03d}" for i in list(range(3, 7)) + list(range(27, 31))]].sum(axis=1)
age_u5 = b01[["c003", "c027"]].sum(axis=1)
fem1544 = b01[[f"c{i:03d}" for i in range(30, 39)]].sum(axis=1)
cov = pd.DataFrame({"pop_acs": pop.pop_acs, "share_65plus": age65 / b01.c001, "share_under18": age_u18 / b01.c001, "share_under5": age_u5 / b01.c001,
                    "share_female_15_44": fem1544 / b01.c001})
b17 = acs("b17001", [1, 2]); cov["poverty_rate"] = b17.c002 / b17.c001
b19 = acs("b19013", [1]); cov["median_hh_income"] = b19.c001
b08 = acs("b08201", [1, 2]); cov["share_hh_no_vehicle"] = b08.c002 / b08.c001
c16 = acs("c16001", [1] + [5 + 3 * k for k in range(12)])
cov["lep_share_5plus"] = c16[[f"c{5 + 3 * k:03d}" for k in range(12)]].sum(axis=1) / c16.c001
b27 = acs("b27001", [1] + [5 + 3 * k for k in range(9)] + [33 + 3 * k for k in range(9)])
no_ins = b27[[f"c{5 + 3 * k:03d}" for k in range(9)] + [f"c{33 + 3 * k:03d}" for k in range(9)]].sum(axis=1)
cov["uninsured_rate"] = no_ins / b27.c001
cov = cov.reindex(zs)

# PLACES
P = RAW / "X_cdc_places_zcta" / "kee5-23sr_places_zcta.csv"
meas = ["DIABETES", "CHD", "BPHIGH", "DEPRESSION", "CHECKUP", "ACCESS2", "CASTHMA", "COPD", "OBESITY", "MHLTH", "PHLTH", "DISABILITY", "LACKTRPT", "CSMOKING", "GHLTH", "DENTAL", "CANCER", "STROKE"]
pl = pd.read_csv(P, dtype={"ZCTA5": str}, usecols=["ZCTA5", "TotalPopulation"] + [f"{m}_CrudePrev" for m in meas]).set_index("ZCTA5")
pl = pl.reindex(zs).rename(columns={"TotalPopulation": "pop_places"})
for m in meas: pl = pl.rename(columns={f"{m}_CrudePrev": f"places_{m.lower()}"})
pl["places_nocheckup"] = 100 - pl.places_checkup
cov = cov.join(pl)

# RUCA (ZIP code with same 5 digits as ZCTA)
ru = pd.read_csv(RAW / "X_usda_ruca_zip/2020-rural-urban-commuting-area-codes-zip-codes.csv", dtype=str).rename(columns={"ZIPCode": "zcta", "PrimaryRUCA": "ruca"})
ru["ruca"] = pd.to_numeric(ru.ruca, errors="coerce")
cov["ruca"] = ru.drop_duplicates("zcta").set_index("zcta").ruca.reindex(zs)

# density
cov["land_km2"] = base.set_index("zcta").aland_m2 / 1e6
b_ = base.set_index("zcta")
cov["elig_per_km2"] = b_.elig_primary / cov.land_km2
cov["elig_per_pop"] = b_.elig_primary / cov.pop_acs.where(cov.pop_acs >= 100)                 # Medi-Cal enrolment rate (can exceed 1 when ZIP != ZCTA)
cov["pop_per_km2"] = cov.pop_acs / cov.land_km2

# HPSA via tract-ZCTA overlap (Census 2020 relationship file, land area overlap)
rt = pd.read_csv(RAW / "X_tract_zcta/tab20_zcta520_tract20_natl.txt", sep="|", dtype=str, encoding="utf-8-sig")
rt = rt[rt.GEOID_ZCTA5_20.isin(zs) & rt.GEOID_TRACT_20.notna()].rename(columns={"GEOID_ZCTA5_20": "zcta", "GEOID_TRACT_20": "tract"})
rt["part"] = rt.AREALAND_PART.astype(float)
zland = rt.groupby("zcta").part.sum()
def hpsa(path, label):
    h = con.execute(f"""select "HPSA ID" as hid, "HPSA Status" as status, "Designation Type" as dtype, "HPSA Geography Identification Number" as geo, try_cast("HPSA Score" as double) as score,
                        "HPSA Postal Code" as zipc, "HPSA Name" as hname from read_csv('{path}', all_varchar=true, header=true, null_padding=true, ignore_errors=true)
                        where "Common State County FIPS Code" like '06%' """).df()
    return h
out = {}
for key, fn in [("pc", "G_hpsa_primary_care/BCD_HPSA_FCT_DET_PC.csv"), ("mh", "G_hpsa_mental_health/BCD_HPSA_FCT_DET_MH.csv"), ("dh", "G_hpsa_dental/BCD_HPSA_FCT_DET_DH.csv")]:
    h = hpsa(RAW / fn, key)
    area = h[(h.status == "Designated") & h.geo.str.fullmatch(r"\d{11}", na=False)]
    area_t = area.groupby("geo").score.max()               # max score for a tract across designations
    r = rt.assign(score=rt.tract.map(area_t))
    r["des"] = r.score.notna()
    share = r[r.des].groupby("zcta").part.sum() / zland
    mx = r[r.des].groupby("zcta").score.max()
    out[f"hpsa_{key}_area_share"] = share.reindex(zs).fillna(0.0)
    out[f"hpsa_{key}_max_score"] = mx.reindex(zs)
    # facility designations (POINT) with a postal code
    fac = h[(h.status == "Designated") & (h.geo == "POINT") & h.zipc.notna()]
    fz = fac.zipc.str[:5].value_counts()
    out[f"hpsa_{key}_facility_designations"] = fz.reindex(zs).fillna(0)
    # withdrawn/proposed information: share of tract area with Proposed For Withdrawal
    pw = h[(h.status == "Proposed For Withdrawal") & h.geo.str.fullmatch(r"\d{11}", na=False)].groupby("geo").score.max()
    rr = rt.assign(pw=rt.tract.map(pw)); rr = rr[rr.pw.notna()]
    out[f"hpsa_{key}_proposed_withdrawal_area_share"] = (rr.groupby("zcta").part.sum() / zland).reindex(zs).fillna(0.0)
hp = pd.DataFrame(out, index=zs)
hp["hpsa_pc_any"] = hp.hpsa_pc_area_share >= 0.5
hp["hpsa_mh_any"] = hp.hpsa_mh_area_share >= 0.5
hp["hpsa_dh_any"] = hp.hpsa_dh_area_share >= 0.5
cov = cov.join(hp)

# HRSA health center sites (service delivery, permanent)
h = pd.read_csv(RAW / "X_hrsa_health_center_sites/Health_Center_Service_Delivery_and_LookAlike_Sites.csv", dtype=str, low_memory=False)
hh = h[h["Complete County Name"].isin(["Riverside County", "San Bernardino County"]) & (h["Site Status Description"] == "Active")].copy()
hh = hh[hh["Health Center Location Type Description"].eq("Permanent") & hh["Site Postal Code"].notna()]
hh["zcta"] = hh["Site Postal Code"].str[:5]
hh["is_service"] = hh["Health Center Service Delivery Site Location Setting Description"].notna()
fq = hh.groupby("zcta").size()
cov["hrsa_sites_permanent"] = fq.reindex(zs).fillna(0).astype(int)
cov["hrsa_site_present"] = cov.hrsa_sites_permanent > 0
cov["hrsa_sites_outside_base_zctas"] = int(len(set(hh.zcta) - set(zs)))
cov.index.name = "zcta"
cov.reset_index().to_parquet(PROC / "zcta_covariates.parquet", index=False)
rep = dict(n_zcta=len(cov), missing_acs_pop=int(cov.pop_acs.isna().sum()), missing_poverty=int(cov.poverty_rate.isna().sum()), missing_income=int(cov.median_hh_income.isna().sum()),
           missing_places=int(cov.places_diabetes.isna().sum()), missing_ruca=int(cov.ruca.isna().sum()), hrsa_sites_in_ie=int(len(hh)), hrsa_sites_matched_to_base_zcta=int(hh.zcta.isin(zs).sum()),
           hpsa_pc_zcta_ge50=int(cov.hpsa_pc_any.sum()), hpsa_mh_zcta_ge50=int(cov.hpsa_mh_any.sum()), hpsa_dh_zcta_ge50=int(cov.hpsa_dh_any.sum()),
           elig_per_pop_gt_1=int((cov.elig_per_pop > 1).sum()), elig_per_pop_gt_0_9=int((cov.elig_per_pop > 0.9).sum()),
           no_citizenship_or_nativity_variables_used=True)
update_checks("covariates", rep)
print(rep)
print(cov.describe().T[["count", "mean", "min", "max"]].round(3).to_string())
