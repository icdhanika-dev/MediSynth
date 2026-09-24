from langgraph.graph import StateGraph, END

from workflow.state import DiagnosticState

from agents.radiology_agent import analyze_radiology
from agents.pathology_agent import analyze_pathology
from agents.history_agent import analyze_history
from agents.conflict_agent import find_conflicts
from agents.debate_agent import run_debate
from agents.consensus_agent import generate_consensus


def run_radiology(state: DiagnosticState):

    result = analyze_radiology(
        state["radiology_report"]
    )

    state["analyses"].append(result)

    return state


def run_pathology(state: DiagnosticState):

    result = analyze_pathology(
        state["pathology_report"]
    )

    state["analyses"].append(result)

    return state


def run_history(state: DiagnosticState):

    result = analyze_history(
        state["patient_history"]
    )

    state["analyses"].append(result)

    return state


def run_conflict_detection(state: DiagnosticState):

    conflicts = find_conflicts(
        state["analyses"]
    )

    state["conflicts"] = conflicts

    return state


def run_debate_step(state: DiagnosticState):

    debates = []

    for conflict in state["conflicts"]:

        debate = run_debate(
            conflict,
            state["analyses"]
        )

        debates.append(debate)

    state["debates"] = debates

    return state


def run_consensus_step(state: DiagnosticState):

    result = generate_consensus(
        state["analyses"],
        state["conflicts"],
        state["debates"]
    )

    state["consensus"] = result.model_dump()

    return state


def decide_next_step(state: DiagnosticState):

    if state["conflicts"]:
        return "debate"

    return "consensus"


def build_workflow():

    graph = StateGraph(
        DiagnosticState
    )

    graph.add_node(
        "radiology",
        run_radiology
    )

    graph.add_node(
        "pathology",
        run_pathology
    )

    graph.add_node(
        "history",
        run_history
    )

    graph.add_node(
        "conflict_detection",
        run_conflict_detection
    )

    graph.add_node(
        "debate",
        run_debate_step
    )

    graph.add_node(
        "consensus",
        run_consensus_step
    )

    graph.set_entry_point(
        "radiology"
    )

    graph.add_edge(
        "radiology",
        "pathology"
    )

    graph.add_edge(
        "pathology",
        "history"
    )

    graph.add_edge(
        "history",
        "conflict_detection"
    )

    graph.add_conditional_edges(
        "conflict_detection",
        decide_next_step,
        {
            "debate": "debate",
            "consensus": "consensus"
        }
    )

    graph.add_edge(
        "debate",
        "consensus"
    )

    graph.add_edge(
        "consensus",
        END
    )

    return graph.compile()


# Create the compiled workflow
workflow = build_workflow()