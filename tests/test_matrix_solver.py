import unittest

from matrix_solver import solve


class MatrixSolverTest(unittest.TestCase):
    def setUp(self):
        self.model = {
            "processes": [
                {
                    "id": "part", "reference_amount": 1, "reference_unit": "kg",
                    "inputs": [{"provider_id": "electricity", "amount": 2, "unit": "kWh"}],
                    "emissions": [{"flow_id": "co2", "amount": 0.5, "unit": "kg"}],
                },
                {
                    "id": "electricity", "reference_amount": 1, "reference_unit": "kWh",
                    "inputs": [],
                    "emissions": [{"flow_id": "co2", "amount": 0.4, "unit": "kg"}],
                },
            ],
            "demand": [{"process_id": "part", "amount": 1}],
            "climate_flows": ["co2"],
            "characterization_factors": {"co2": 1},
        }

    def test_upstream_supplier_is_scaled_once(self):
        result = solve(self.model)
        self.assertAlmostEqual(result["gwp100_kg_co2e"], 1.3)
        self.assertAlmostEqual(result["process_scaling"]["electricity"], 2)
        self.assertAlmostEqual(result["technology_residual_max"], 0)

    def test_missing_supplier_fails(self):
        self.model["processes"][0]["inputs"][0]["provider_id"] = "absent"
        with self.assertRaisesRegex(ValueError, "missing upstream provider"):
            solve(self.model)

    def test_unit_mismatch_fails(self):
        self.model["processes"][0]["inputs"][0]["unit"] = "MJ"
        with self.assertRaisesRegex(ValueError, "unit mismatch"):
            solve(self.model)

    def test_missing_climate_factor_fails(self):
        self.model["characterization_factors"] = {}
        with self.assertRaisesRegex(ValueError, "missing characterization factor"):
            solve(self.model)


if __name__ == "__main__":
    unittest.main()
