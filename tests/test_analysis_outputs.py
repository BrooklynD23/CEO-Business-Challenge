"""Real assertions on the Phase 1 analysis outputs. Run:  $HOME/.venvs/iehp-access/bin/python -I tests/test_analysis_outputs.py
(stdlib unittest; pytest is not installed in this environment)."""
import json, sys, unittest
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC, TAB, QUAL = ROOT / "data/processed", ROOT / "outputs/tables", ROOT / "data/quality"


class TestBaseTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = pd.read_parquet(PROC / "base_table.parquet")
        cls.checks = json.load(open(QUAL / "checks.json"))

    def test_169_ie_touching_zctas_unique_text_keys(self):
        self.assertEqual(len(self.base), 169)
        self.assertTrue(self.base.zcta.is_unique)
        self.assertTrue(self.base.zcta.str.fullmatch(r"\d{5}").all())
        self.assertTrue(self.base.zip.dropna().str.fullmatch(r"\d{5}").all())

    def test_eligibles_sum_matches_data_report(self):
        # data report: A's IE-touching ZCTA total for 2026-09 is 1,871,886
        self.assertEqual(int(self.base.elig_primary.sum()), 1_871_886)

    def test_missing_zcta_is_89019_and_suppression_is_not_zero(self):
        self.assertEqual(self.base[~self.base.in_A].zcta.tolist(), ["89019"])
        sup = self.base[self.base.is_suppressed & self.base.in_A]
        self.assertTrue(sup.elig_primary.isna().all(), "suppressed cells must stay missing, never zero")

    def test_population_share_allocation_matches_county_totals(self):
        rec = pd.read_csv(TAB / "s01_reconciliation_A_vs_B.csv")
        r = rec[rec.month == "2026-09"]
        for _, row in r.iterrows():
            self.assertLess(abs(row.A_pop_share_alloc / row.B_total - 1), 0.01)

    def test_guide_overshoot_about_three_percent(self):
        o = self.checks["base_table"]["touching_overshoot"]["2026-09"]["pct_over"]
        self.assertAlmostEqual(o, 3.0, delta=0.2)


class TestSupply(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = pd.read_parquet(PROC / "provider_classified.parquet")
        cls.ie = cls.c[cls.c.in_ie]

    def test_ie_extract_matches_data_report(self):
        self.assertEqual(len(self.ie), 36_470)
        real = self.ie.loc[~self.ie.npi_key.str.startswith("PN"), "npi_key"]
        self.assertEqual(real.nunique(), 30_520)      # 2 rows have blank/0 NPI and carry a provider-number fallback key (PN...)
        self.assertEqual(int(self.ie.npi_key.str.startswith("PN").sum()), 2)

    def test_definitions_are_nested(self):
        for g in ["pcp", "pcp_md", "mh", "specialist_all"]:
            a, b, cc, d = (self.ie[f"w_{g}__{x}"].sum() for x in "abcd")
            self.assertGreaterEqual(a, b); self.assertGreaterEqual(b, cc); self.assertGreaterEqual(cc, d)
            self.assertLessEqual(self.ie[f"w_{g}__e"].sum(), b + 1e-6)

    def test_orp_source3_excluded_from_deduped_supply(self):
        s3 = self.ie[self.ie.source == "3"]
        for g in ["pcp", "mh", "specialist_all"]:
            self.assertEqual(s3[f"w_{g}__b"].sum(), 0)

    def test_no_provider_names_or_phones_in_processed_file(self):
        banned = {"legal_name", "phone", "address", "provider_website"}
        self.assertFalse(banned & {c.lower() for c in self.c.columns})


class TestScenarios(unittest.TestCase):
    def test_guide_rounding(self):
        base = 1_321_983
        self.assertEqual(round(base * 0.14), 185_078)
        self.assertEqual(round(base / 7), 188_855)
        sc = pd.read_csv(TAB / "s04_scenarios_movers.csv")
        self.assertIn(100_000, sc.movers.tolist()); self.assertIn(132_000, sc.movers.tolist()); self.assertIn(155_000, sc.movers.tolist())

    def test_all_plan_exceeds_iehp_only(self):
        ap = pd.read_csv(TAB / "s04_all_plan_mover_scenarios.csv")
        self.assertTrue((ap.all_plan_movers > ap.iehp_movers).all())

    def test_existing_ffs_published_value(self):
        s = pd.read_csv(TAB / "s04_existing_ffs_series_two_counties.csv", index_col=0)
        self.assertEqual(int(s.loc["2026-09", "Riverside"]), 52_453); self.assertEqual(int(s.loc["2026-09", "San Bernardino"]), 46_753)


class TestRankingAndGuards(unittest.TestCase):
    def test_ranking_complete_and_ranks_valid(self):
        r = pd.read_parquet(PROC / "gap_ranking.parquet")
        self.assertEqual(len(r), 130); self.assertTrue(r.zcta.is_unique)
        self.assertEqual(int(r.rank_equal.min()), 1); self.assertTrue((r.rank_equal <= 130).all())
        self.assertTrue((r.top_decile_freq_weight_sweep.between(0, 1)).all())

    def test_sensitive_variable_guard_passed(self):
        with open(QUAL / "checks.json") as fh:
            q = json.load(fh)["quality"]
        self.assertTrue(q["sensitive_column_guard"]["passed"])

    def test_raw_ratio_uses_all_eligibles_denominator(self):
        a = pd.read_parquet(PROC / "access_measures.parquet").dropna(subset=["raw_per1000_pcp__b", "elig_2026_09"])
        calc = a["n_pcp__b"] / a["elig_2026_09"] * 1000
        self.assertLess((calc - a["raw_per1000_pcp__b"]).abs().max(), 1e-9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
