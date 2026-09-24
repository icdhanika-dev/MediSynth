from graph.graph_builder import build_evidence_graph
from models.schemas import AgentAnalysis, Finding


radiology = AgentAnalysis(
    agent="radiology",
    findings=[
        Finding(
            finding="Right lower lobe opacity",
            evidence="Chest X-ray shows a focal opacity",
            confidence=0.84
        )
    ],
    possible_conditions=["Pneumonia"],
    uncertainties=["Cause of opacity is not completely certain"],
    contradictions=[]
)


pathology = AgentAnalysis(
    agent="pathology",
    findings=[
        Finding(
            finding="Chronic inflammatory cell infiltration",
            evidence="Histopathology shows inflammatory cell infiltration",
            confidence=0.78
        )
    ],
    possible_conditions=["Chronic inflammatory process"],
    uncertainties=[],
    contradictions=[]
)


analyses = [radiology, pathology]

build_evidence_graph("TEST_CASE_001", analyses)