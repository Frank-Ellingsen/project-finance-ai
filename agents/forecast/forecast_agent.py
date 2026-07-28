from pydantic import BaseModel
from typing import Dict, Any, List

class ForecastInput(BaseModel):
    validated_dataset: Dict[str, Any]
    assumptions: Dict[str, Any]

class ForecastOutput(BaseModel):
    eac: Dict[str, float]
    etc: Dict[str, float]
    rolling_forecast: List[Dict[str, float]]
    scenarios: List[Dict[str, Any]]
    commentary: str

class ForecastAgent:
    """
    Personality: Analytical, cautious, assumption-driven.
    Constraints: - Never modifies source data. - Must show assumptions explicitly. - Must produce base/optimistic/pessimistic scenarios.
    """
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("Forecast Agent: Modeling EAC, ETC and scenarios...")
        return {
            "project_id": "P-1023",
            "period": "2026-06",
            "eac_cost": 1420000,
            "eac_revenue": 1308000,
            "eac_margin": -112000,
            "etc_cost": 160000,
            "etc_revenue": 23000,
            "commentary": "EAC/ETC calculated based on cost burn rate."
        }
