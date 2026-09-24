class PathologyAgent:
    def __init__(self):
        self.name = "Pathology Agent"

    def analyze(self, pathology_report):
        if not pathology_report:
            return {
                "agent": self.name,
                "finding": "No pathology report provided",
                "confidence": 0.0
            }

        findings = {
            "agent": self.name,
            "finding": "Pathology evidence analyzed",
            "evidence": pathology_report,
            "confidence": 0.80
        }

        return findings
