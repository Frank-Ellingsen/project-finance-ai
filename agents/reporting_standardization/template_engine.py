from pydantic import BaseModel
from typing import Dict, Any, List

class ReportingInput(BaseModel):
    bi_spec: Dict[str, Any]

class ReportingOutput(BaseModel):
    template_structure: List[str]
    field_mapping: Dict[str, List[str]]
    process_steps: List[str]
    governance_rules: List[str]

class ReportingStandardizationAgent:
    """
    Personality: Process-driven, governance-minded.
    Constraints: - Must enforce cross-project comparability. - Cannot change business rules. - Must produce reusable templates.
    """
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("Reporting Standardization Agent: Compiling report template...")
        return {
            "template_structure": ["Executive Summary", "Financial Overview", "Forecast Overview", "Risk Overview"],
            "field_mapping": {
                "Executive Summary": ["margin_variance_abs", "risk_level"],
                "Forecast Overview": ["eac_cost", "eac_margin"]
            }
        }
