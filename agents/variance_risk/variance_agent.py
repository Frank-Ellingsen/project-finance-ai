from pydantic import BaseModel
from typing import Dict, Any, List

class VarianceRiskInput(BaseModel):
    validated_dataset: Dict[str, Any]
    forecast_package: Dict[str, Any]

class VarianceRiskOutput(BaseModel):
    variance: Dict[str, Any]
    drivers: List[Dict[str, Any]]
    risk_exposure: Dict[str, Any]
    summary: str

class VarianceRiskAgent:
    """
    Personality: Investigative, pattern-seeking.
    Constraints: - Must distinguish data issues from real business issues. - Cannot assign blame. - Must quantify risk exposure.
    """
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("Variance & Risk Agent: Analyzing cost overruns and identifying risks...")
        return {
            "project_id": "P-1023",
            "period": "2026-06",
            "cost_variance_abs": 89000,
            "cost_variance_pct": 7.6,
            "risk_level": "High",
            "drivers": [
                {"driver_name": "Material price increase", "driver_type": "price", "impact": -42000},
                {"driver_name": "Labor overrun", "driver_type": "volume", "impact": -38000}
            ]
        }
