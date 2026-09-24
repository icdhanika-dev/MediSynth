from llm_client import call_llm_json
from models.schemas import AgentAnalysis


def analyze_history(history: str) -> AgentAnalysis:

    prompt = f"""
You are the patient-history specialist in a medical
decision-support system.

Analyze the following patient history:

{history}

Focus only on information from the patient's history.

Identify:
- important symptoms and medical history
- relevant risk factors
- evidence from the history
- possible conditions suggested by the history
- uncertainties
- contradictions

Do not invent information.
Confidence must be a number between 0 and 1.
"""

    data = call_llm_json(prompt,"history")

    return AgentAnalysis(**data)