from pydantic import BaseModel
from typing import Dict, Any, List

class DecisionInput(BaseModel):
    standardized_report: Dict[str, Any]

class DecisionOutput(BaseModel):
    situation_summary: str
    options: List[Dict[str, Any]]
    impact_analysis: List[Dict[str, Any]]
    recommendation: str

class DecisionSupportAgent:
    """
    Personality: Executive-oriented, concise.
    Constraints: - Must present multiple options. - Cannot make decisions. - Must avoid technical jargon.
    """
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("Decision Support Agent: Formulating executive decision memo...")
        return {
            "situation_summary": "P-1023 is facing margin pressure due to materials price increases.",
            "options": [
                {"option_name": "Accelerate subcontractor work", "impact": "Medium risk, cost impact -45k"},
                {"option_name": "Reduce scope", "impact": "Low risk, customer concern"}
            ],
            "recommendation": "Accelerate subcontractor work to mitigate schedule delay risk."
        }
