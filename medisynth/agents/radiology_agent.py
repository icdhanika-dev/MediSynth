<<<<<<< HEAD
from llm_client import call_vision_llm_json
from models.schemas import AgentAnalysis


def analyze_radiology(image_url: str) -> AgentAnalysis:

    prompt = """
You are the radiology specialist in a medical
decision-support system.

Analyze the uploaded radiology image.

Focus only on visible radiological findings.

Identify:
- important imaging findings
- evidence visible in the image
- possible conditions suggested by the findings
- uncertainties
- contradictions

Do not invent information that cannot be supported
by the image.

Do not give a definitive diagnosis.

Confidence must be a number between 0 and 1.

Return only valid JSON using this structure:

{
    "agent": "radiology",
    "findings": [
        {
            "finding": "string",
            "evidence": "string",
            "confidence": 0.0
        }
    ],
    "possible_conditions": [
        "string"
    ],
    "uncertainties": [
        "string"
    ],
    "contradictions": [
        "string"
    ]
}
"""

    data = call_vision_llm_json(
        prompt,
        image_url
    )

    return AgentAnalysis(**data)
=======
class RadiologyAgent:
    def __init__(self):
        self.name = "Radiology Agent"

    def analyze(self, radiology_report):
        if not radiology_report:
            return {
                "agent": self.name,
                "finding": "No radiology report provided",
                "confidence": 0.0
            }

        findings = {
            "agent": self.name,
            "finding": "Radiology evidence analyzed",
            "evidence": radiology_report,
            "confidence": 0.80
        }

        return findings
>>>>>>> origin/main
