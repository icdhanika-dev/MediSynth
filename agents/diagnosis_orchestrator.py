class DiagnosisOrchestrator:

    def __init__(self):
        self.name = "Diagnosis Orchestrator"

    def analyze(self, patient_history, radiology_result, pathology_result):

        results = {
            "patient_history": patient_history,
            "radiology": radiology_result,
            "pathology": pathology_result
        }

        # Collect findings from all specialist agents
        findings = []

        for agent, result in results.items():
            if result:
                findings.append({
                    "agent": agent,
                    "finding": result
                })

        # Simple reconciliation
        consolidated = {
            "agent": self.name,
            "specialist_findings": findings,
            "status": "Requires physician review",
            "message": (
                "Findings from patient history, radiology and pathology "
                "agents have been collected for clinical review."
            )
        }

        return consolidated
