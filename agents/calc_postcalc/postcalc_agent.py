from pydantic import BaseModel
from typing import Dict, Any, List

class CalcInput(BaseModel):
    bid_data: Dict[str, Any]
    actuals: Dict[str, Any]
    historical_projects: List[Dict[str, Any]]

class CalcOutput(BaseModel):
    bid_summary: Dict[str, Any]
    post_calc_comparison: List[Dict[str, Any]]
    lessons_learned: List[str]
    suggested_updates: List[str]

class CalculationPostCalcAgent:
    """
    Personality: Cost-focused, benchmark-aware.
    Constraints: - Must explain assumptions. - Cannot submit bids. - Must compare bid vs actual transparently.
    """
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("Calculation & Post-Calc Agent: Comparing bid assumptions with actual performance...")
        return {
            "lessons_learned": [
                "Material price volatility underestimated",
                "Labor productivity assumptions too optimistic"
            ],
            "suggested_updates": [
                "Increase material contingency from 5% to 8%",
                "Add productivity buffer for labor (10%)"
            ]
        }
