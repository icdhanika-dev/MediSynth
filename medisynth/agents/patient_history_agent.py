class PatientHistoryAgent:

    def __init__(self):
        self.name = "Patient History Agent"

    def analyze(self, patient_history):

        if not patient_history:
            return {
                "agent": self.name,
                "finding": "No patient history provided",
                "confidence": 0.0
            }

        findings = {
            "agent": self.name,
            "finding": "Patient history analyzed",
            "evidence": patient_history,
            "confidence": 0.80
        }

        return findings
