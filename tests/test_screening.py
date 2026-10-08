"""Checks for failures that would make a screening total misleading."""

import copy
import json
import unittest

from kettle_lca import BOM, read_csv
from screening import CONFIG, INPUTS, calculate


class ScreeningChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(CONFIG.read_text())
        cls.bom = read_csv(BOM)
        cls.inputs = read_csv(INPUTS)

    def test_balance_and_stage_sum(self):
        run = calculate("central", self.bom, self.inputs, self.config)
        rows = run["material_breakdown"]
        self.assertAlmostEqual(sum(x["finished_kg"] for x in rows), 0.8608)
        self.assertAlmostEqual(sum(x["purchased_kg"] - x["scrap_kg"] for x in rows), 0.8608)
        self.assertAlmostEqual(sum(run["stage_contributions"].values()), run["screening_gwp100_kgco2e_per_packaged_kettle"])

    def test_missing_material_or_unmarked_factor_fails(self):
        with self.assertRaises(ValueError):
            calculate("central", self.bom, self.inputs[:-1], self.config)
        changed = copy.deepcopy(self.inputs)
        changed[0]["factor_status"] = "sourced"
        with self.assertRaises(ValueError):
            calculate("central", self.bom, changed, self.config)

    def test_inconsistent_yield_fails(self):
        changed = copy.deepcopy(self.inputs)
        changed[0]["procurement_ratio"] = "1.0"
        with self.assertRaises(ValueError):
            calculate("central", self.bom, changed, self.config)


if __name__ == "__main__":
    unittest.main()
