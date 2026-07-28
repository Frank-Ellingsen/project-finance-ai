import os
import csv
from agents.erp_data_foundation.erp_connector import ERPDataFoundationAgent
from agents.forecast.forecast_agent import ForecastAgent
from agents.variance_risk.variance_agent import VarianceRiskAgent
from agents.power_bi.dax_generator import PowerBIAgent
from agents.reporting_standardization.template_engine import ReportingStandardizationAgent
from agents.decision_support.decision_agent import DecisionSupportAgent
from agents.calc_postcalc.postcalc_agent import CalculationPostCalcAgent

# Helper to load CSV using Python's standard library
def load_csv(filename):
    filepath = os.path.join("mock_data", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# ---------------------------------------------------------
# 1. Load mock CSV data
# ---------------------------------------------------------
print("Loading mock data...")

erp_raw = load_csv("erp_raw_data.csv")
validated = load_csv("validated_dataset.csv")
forecast_input = load_csv("forecast_input.csv")
forecast_output = load_csv("forecast_output.csv")
rolling_forecast = load_csv("rolling_forecast.csv")
variance_report = load_csv("variance_risk_report.csv")
variance_drivers = load_csv("variance_drivers.csv")
risk_items = load_csv("risk_items.csv")
powerbi_kpis = load_csv("powerbi_kpis.csv")
standardized_report = load_csv("standardized_report.csv")
decision_support = load_csv("decision_support.csv")
postcalc_comparison = load_csv("postcalc_comparison.csv")
lessons_learned = load_csv("lessons_learned.csv")
suggested_updates = load_csv("suggested_updates.csv")

# Convert numeric strings where appropriate for the mock run
def clean_record(rec):
    cleaned = {}
    for k, v in rec.items():
        try:
            if "." in v:
                cleaned[k] = float(v)
            else:
                cleaned[k] = int(v)
        except ValueError:
            cleaned[k] = v
    return cleaned

# ---------------------------------------------------------
# 2. Initialize agents
# ---------------------------------------------------------
erp_agent = ERPDataFoundationAgent()
forecast_agent = ForecastAgent()
variance_agent = VarianceRiskAgent()
powerbi_agent = PowerBIAgent()
report_agent = ReportingStandardizationAgent()
decision_agent = DecisionSupportAgent()
postcalc_agent = CalculationPostCalcAgent()

# ---------------------------------------------------------
# 3. Simulate LangGraph state
# ---------------------------------------------------------
state = {
    "validated_dataset": clean_record(validated[0]),
    "forecast_package": clean_record(forecast_output[0]),
    "variance_risk_report": clean_record(variance_report[0]),
    "needs_calc": True # simulate conditional branch
}

# ---------------------------------------------------------
# 4. Run pipeline
# ---------------------------------------------------------
print("\n=== ERP & Data Foundation Agent ===")
erp_out = erp_agent.run(state["validated_dataset"])
print(erp_out)

print("\n=== Forecast Agent ===")
forecast_out = forecast_agent.run({
    "validated_dataset": state["validated_dataset"],
    "assumptions": {
        "remaining_work": state["validated_dataset"].get("remaining_work_estimate", 0.22),
        "risk_adjustment": state["validated_dataset"].get("risk_adjustment", 0.05)
    }
})
print(forecast_out)

print("\n=== Variance & Risk Agent ===")
variance_out = variance_agent.run({
    "validated_dataset": state["validated_dataset"],
    "forecast_package": state["forecast_package"]
})
print(variance_out)

print("\n=== Power BI Agent ===")
powerbi_out = powerbi_agent.run({
    "forecast_package": state["forecast_package"],
    "variance_risk_report": state["variance_risk_report"]
})
print(powerbi_out)

print("\n=== Reporting Standardization Agent ===")
report_out = report_agent.run({
    "bi_spec": powerbi_out
})
print(report_out)

print("\n=== Decision Support Agent ===")
decision_out = decision_agent.run({
    "standardized_report": report_out
})
print(decision_out)

# ---------------------------------------------------------
# 5. Conditional branch: Post-Calc Agent
# ---------------------------------------------------------
if state["needs_calc"]:
    print("\n=== Calculation & Post-Calc Agent ===")
    postcalc_out = postcalc_agent.run({
        "bid_data": {}, # mock
        "actuals": state["validated_dataset"],
        "historical_projects": []
    })
    print(postcalc_out)

    print("\nFeedback loop -> ERP Agent")
    erp_feedback = erp_agent.run(postcalc_out)
    print(erp_feedback)

print("\n=== Pipeline Simulation Complete ===")
