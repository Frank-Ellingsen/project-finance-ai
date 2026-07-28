import unittest
import sys
import os

# Add root folder to sys path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.erp_data_foundation.erp_connector import ERPDataFoundationAgent
from agents.forecast.forecast_agent import ForecastAgent
from agents.variance_risk.variance_agent import VarianceRiskAgent
from agents.power_bi.dax_generator import PowerBIAgent
from agents.reporting_standardization.template_engine import ReportingStandardizationAgent
from agents.decision_support.decision_agent import DecisionSupportAgent
from agents.calc_postcalc.postcalc_agent import CalculationPostCalcAgent

class TestERPDataFoundationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ERPDataFoundationAgent()

    def test_run_valid_data(self):
        input_data = {
            "project_id": "P-1023",
            "period": "2026-06",
            "total_budget_cost": 1170000,
            "total_actual_cost": 1259000,
            "remaining_work_estimate": 0.22,
            "risk_adjustment": 0.05
        }
        output = self.agent.run(input_data)
        self.assertEqual(output["status"], "Validated")
        self.assertEqual(output["project_id"], "P-1023")
        self.assertEqual(output["total_budget_cost"], 1170000)

class TestForecastAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ForecastAgent()

    def test_run_generates_forecast(self):
        input_data = {
            "validated_dataset": {
                "project_id": "P-1023",
                "period": "2026-06",
                "total_budget_cost": 1170000
            }
        }
        output = self.agent.run(input_data)
        self.assertEqual(output["project_id"], "P-1023")
        self.assertIn("eac_cost", output)
        self.assertIn("etc_cost", output)

class TestVarianceRiskAgent(unittest.TestCase):
    def setUp(self):
        self.agent = VarianceRiskAgent()

    def test_run_analyses_variance(self):
        input_data = {
            "validated_dataset": {},
            "forecast_package": {}
        }
        output = self.agent.run(input_data)
        self.assertEqual(output["project_id"], "P-1023")
        self.assertEqual(output["risk_level"], "High")
        self.assertGreater(len(output["drivers"]), 0)

class TestPowerBIAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PowerBIAgent()

    def test_run_generates_dax(self):
        input_data = {}
        output = self.agent.run(input_data)
        self.assertIn("dax_measures", output)
        self.assertTrue(any(m["kpi_name"] == "Total Cost" for m in output["dax_measures"]))

class TestReportingStandardizationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ReportingStandardizationAgent()

    def test_run_compiles_template(self):
        input_data = {}
        output = self.agent.run(input_data)
        self.assertIn("template_structure", output)
        self.assertIn("field_mapping", output)

class TestDecisionSupportAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DecisionSupportAgent()

    def test_run_formulates_memo(self):
        input_data = {}
        output = self.agent.run(input_data)
        self.assertIn("situation_summary", output)
        self.assertIn("recommendation", output)

class TestCalculationPostCalcAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CalculationPostCalcAgent()

    def test_run_compares_bid(self):
        input_data = {}
        output = self.agent.run(input_data)
        self.assertIn("lessons_learned", output)
        self.assertIn("suggested_updates", output)

if __name__ == "__main__":
    unittest.main()
