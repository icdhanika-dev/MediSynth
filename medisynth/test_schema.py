from models.schemas import Finding, AgentAnalysis


finding = Finding(
    finding="Right lower lobe opacity",
    evidence="Chest X-ray shows a localized opacity",
    confidence=0.84
)


analysis = AgentAnalysis(
    agent="radiology",
    findings=[finding],
    possible_conditions=["Pneumonia"],
    uncertainties=["Cause of opacity is not completely certain"],
    contradictions=[]
)


print("\nSCHEMA TEST PASSED")
print(analysis.model_dump())