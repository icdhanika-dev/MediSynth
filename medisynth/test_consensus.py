from models.schemas import AgentAnalysis
from agents.conflict_agent import find_conflicts
from agents.debate_agent import run_debate
from agents.consensus_agent import generate_consensus


radiology = AgentAnalysis(
    agent="radiology",
    findings=[],
    possible_conditions=["Pneumonia"],
    uncertainties=["The opacity is not completely specific"],
    contradictions=[]
)

pathology = AgentAnalysis(
    agent="pathology",
    findings=[],
    possible_conditions=["Chronic inflammation"],
    uncertainties=["The exact cause is unclear"],
    contradictions=[]
)

history = AgentAnalysis(
    agent="history",
    findings=[],
    possible_conditions=["Pneumonia"],
    uncertainties=[],
    contradictions=[]
)


analyses = [radiology, pathology, history]

conflicts = find_conflicts(analyses)

debates = []

if conflicts:
    debate = run_debate(conflicts[0], analyses)
    debates.append(debate)


result = generate_consensus(
    analyses,
    conflicts,
    debates
)

print("\nCONSENSUS RESULT")
print(result.model_dump())