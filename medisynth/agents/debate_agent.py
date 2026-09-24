from llm_client import call_llm
from models.schemas import DebateResult


def run_debate(conflict: dict, analyses: list) -> DebateResult:

    agent_a = conflict["agent_a"]
    agent_b = conflict["agent_b"]

    analysis_a = next(
        analysis for analysis in analyses
        if analysis.agent == agent_a
    )

    analysis_b = next(
        analysis for analysis in analyses
        if analysis.agent == agent_b
    )

    prompt = f"""
You are a debate coordinator in a medical decision-support system.

Two specialist agents disagree about a medical case.

Agent A: {agent_a}
Possible conditions:
{analysis_a.possible_conditions}

Findings:
{analysis_a.findings}

Agent B: {agent_b}
Possible conditions:
{analysis_b.possible_conditions}

Findings:
{analysis_b.findings}

Conflict:
{conflict["reason"]}

Analyze the disagreement.

For each agent:
- state its position
- identify the evidence supporting that position
- explain the other agent's position
- respond to the opposing evidence
- give a revised position if necessary

Do not invent medical information.

Finally, provide a neutral conclusion explaining:
- which evidence is stronger
- what remains uncertain
- whether the disagreement is resolved

Return only valid JSON.

Use this structure:

{{
    "topic": "string",
    "participants": ["string"],
    "positions": ["string"],
    "evidence": ["string"],
    "responses": ["string"],
    "revised_positions": ["string"],
    "conclusion": "string"
}}
"""

    result = call_llm(prompt)

    import json

    try:
        data = json.loads(result)
    except json.JSONDecodeError:
        start = result.find("{")
        end = result.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("Debate agent did not return valid JSON.")

        data = json.loads(result[start:end])

    return DebateResult(**data)