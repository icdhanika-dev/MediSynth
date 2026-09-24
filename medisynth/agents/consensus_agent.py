import json

from llm_client import call_llm
from models.schemas import ConsensusResult


def generate_consensus(analyses: list, conflicts: list, debates: list):

    analysis_text = []

    for analysis in analyses:
        analysis_text.append({
            "agent": analysis.agent,
            "findings": [
                finding.model_dump()
                for finding in analysis.findings
            ],
            "possible_conditions": analysis.possible_conditions,
            "uncertainties": analysis.uncertainties,
            "contradictions": analysis.contradictions
        })

    prompt = f"""
You are the consensus coordinator in a medical
decision-support system.

You have received independent analyses from
specialist agents.

SPECIALIST ANALYSES:
{json.dumps(analysis_text, indent=2)}

DETECTED CONFLICTS:
{json.dumps(conflicts, indent=2)}

DEBATE RESULTS:
{json.dumps(
    [debate.model_dump() for debate in debates],
    indent=2
)}

Create a consolidated differential for a human doctor.

Important rules:
- Do not invent medical information.
- Do not present the result as a final diagnosis.
- Consider evidence from all agents.
- Consider the debate when resolving conflicts.
- Clearly mention unresolved disagreements.
- Identify missing evidence.
- Confidence must be between 0 and 1.

Return only valid JSON.

Use this structure:

{{
    "consensus": "string",
    "differential": ["string"],
    "supporting_evidence": ["string"],
    "unresolved_conflicts": ["string"],
    "confidence": 0.0,
    "evidence_gaps": ["string"]
}}
"""

    result = call_llm(prompt)

    try:
        data = json.loads(result)

    except json.JSONDecodeError:
        start = result.find("{")
        end = result.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError(
                "Consensus agent did not return valid JSON."
            )

        data = json.loads(result[start:end])

    return ConsensusResult(**data)