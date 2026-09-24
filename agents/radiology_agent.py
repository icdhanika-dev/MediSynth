class RadiologyAgent:
    def __init__(self):
        self.name = "Radiology Agent"

    def analyze(self, radiology_report):
        if not radiology_report:
            return {
                "agent": self.name,
                "finding": "No radiology report provided",
                "confidence": 0.0
            }

        findings = {
            "agent": self.name,
            "finding": "Radiology evidence analyzed",
            "evidence": radiology_report,
            "confidence": 0.80
        }

        return findings
