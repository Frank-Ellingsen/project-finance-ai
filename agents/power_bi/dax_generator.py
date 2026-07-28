from pydantic import BaseModel
from typing import Dict, Any, List

class PowerBIInput(BaseModel):
    forecast_package: Dict[str, Any]
    variance_risk_report: Dict[str, Any]

class PowerBIOutput(BaseModel):
    data_model: Dict[str, Any]
    dax_measures: List[Dict[str, str]]
    dashboard_layout: List[Dict[str, Any]]
    usage_notes: str

class PowerBIAgent:
    """
    Personality: Structured, technical, UX-conscious.
    Constraints: - Must maintain KPI consistency. - Avoid overly complex DAX. - Cannot publish dashboards—only generate specs.
    """
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("Power BI Agent: Generating DAX metrics...")
        return {
            "dax_measures": [
                {"kpi_name": "Total Cost", "dax": "SUM(FactCosts[ActualCost])"},
                {"kpi_name": "Margin", "dax": "[Total Revenue] - [Total Cost]"}
            ]
        }
