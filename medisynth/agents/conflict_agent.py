import json

from llm_client import call_llm
from models.schemas import AgentAnalysis


def local_conflict_check(first: AgentAnalysis, second: AgentAnalysis):

    first_conditions = {
        condition.lower().strip()
        for condition in first.possible_conditions
    }

    second_conditions = {
        condition.lower().strip()
        for condition in second.possible_conditions
    }

    if not first_conditions or not second_conditions:
        return {
            "is_conflict": False,
            "severity": "low",
            "reason": ""
        }

    common = first_conditions & second_conditions

    if common:
        return {
            "is_conflict": False,
            "severity": "low",
            "reason": ""
        }

    return {
        "is_conflict": True,
        "severity": "medium",
        "reason": (
            "The specialist agents suggested different possible "
            "conditions based on their available evidence."
        )
    }


def check_pair(first: AgentAnalysis, second: AgentAnalysis):

    prompt = f"""
You are a conflict detection component in a medical
decision-support system.

Compare the two specialist analyses below.

AGENT A: {first.agent}

Findings:
{first.findings}

Possible conditions:
{first.possible_conditions}

Uncertainties:
{first.uncertainties}

Contradictions:
{first.contradictions}


AGENT B: {second.agent}

Findings:
{second.findings}

Possible conditions:
{second.possible_conditions}

Uncertainties:
{second.uncertainties}

Contradictions:
{second.contradictions}


Determine whether the two analyses contain a meaningful
medical disagreement.

Important:
- Different possible conditions do NOT automatically mean
  there is a contradiction.
- Related or compatible conditions should not be marked
  as conflicts.
- Only identify a conflict when the evidence or conclusions
  meaningfully disagree.
- Use only the information provided.
- Do not invent medical facts.

Return only valid JSON.

Use this structure:

{{
    "is_conflict": true,
    "severity": "low",
    "reason": "string"
}}
"""

    try:

        result = call_llm(prompt)

        try:
            return json.loads(result)

        except json.JSONDecodeError:

            start = result.find("{")
            end = result.rfind("}") + 1

            if start == -1 or end == 0:
                raise ValueError(
                    "Conflict detector did not return valid JSON."
                )

            return json.loads(result[start:end])

    except Exception as e:

        print("Conflict detector LLM failed.")
        print("Using local conflict check instead.")

        return local_conflict_check(
            first,
            second
        )


def find_conflicts(analyses: list[AgentAnalysis]) -> list[dict]:

    conflicts = []

    for i in range(len(analyses)):
        for j in range(i + 1, len(analyses)):

            first = analyses[i]
            second = analyses[j]

            result = check_pair(
                first,
                second
            )

            if result.get("is_conflict"):

                conflicts.append({
                    "agent_a": first.agent,
                    "agent_b": second.agent,
                    "reason": result.get("reason", ""),
                    "severity": result.get(
                        "severity",
                        "medium"
                    ),
                    "conditions_a": first.possible_conditions,
                    "conditions_b": second.possible_conditions
                })

    return conflicts