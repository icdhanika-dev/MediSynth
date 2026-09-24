from models.schemas import AgentAnalysis
from agents.conflict_agent import find_conflicts


radiology = AgentAnalysis(
    agent="radiology",
    findings=[],
    possible_conditions=["Pneumonia"],
    uncertainties=[],
    contradictions=[]
)

pathology = AgentAnalysis(
    agent="pathology",
    findings=[],
    possible_conditions=["Chronic inflammation"],
    uncertainties=[],
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

print("\nCONFLICT DETECTOR TEST")
print(conflicts)

from models.schemas import AgentAnalysis
from agents.conflict_agent import find_conflicts


radiology = AgentAnalysis(
    agent="radiology",
    findings=[
        {
            "finding": "Right lower lobe opacity",
            "evidence": "Chest X-ray shows a focal opacity",
            "confidence": 0.90
        }
    ],
    possible_conditions=["Pneumonia"],
    uncertainties=[],
    contradictions=[]
)


pathology = AgentAnalysis(
    agent="pathology",
    findings=[
        {
            "finding": "No evidence of acute inflammation",
            "evidence": "Histopathology shows no acute inflammatory changes",
            "confidence": 0.90
        }
    ],
    possible_conditions=["No acute inflammatory process"],
    uncertainties=[],
    contradictions=[]
)


history = AgentAnalysis(
    agent="history",
    findings=[
        {
            "finding": "Persistent fever and cough",
            "evidence": "Patient reports fever and cough for five days",
            "confidence": 0.85
        }
    ],
    possible_conditions=["Pneumonia"],
    uncertainties=[],
    contradictions=[]
)


analyses = [radiology, pathology, history]

conflicts = find_conflicts(analyses)

print("\nCONFLICT DETECTOR TEST")
print(conflicts)