class PathologyAgent:
    def __init__(self):
        self.name = "Pathology Agent"

    def analyze(self, pathology_report):
        if not pathology_report:
            return {
                "agent": self.name,
                "status": "error",
                "message": "No pathology report provided"
            }

        report = pathology_report.lower()

        findings = []

        # Basic keyword-based extraction
        if "tumor" in report:
            findings.append("Tumor mentioned in the report")

        if "malignant" in report:
            findings.append("Malignancy mentioned in the report")

        if "benign" in report:
            findings.append("Benign finding mentioned in the report")

        if "inflammation" in report:
            findings.append("Inflammation mentioned in the report")

        if "infection" in report:
            findings.append("Infection mentioned in the report")

        if not findings:
            findings.append("No predefined abnormality keywords detected")

        return {
            "agent": self.name,
            "status": "success",
            "findings": findings,
            "evidence": pathology_report
        }


if __name__ == "__main__":
    agent = PathologyAgent()

    sample_report = """
    The pathology report shows inflammation.
    No malignant cells were identified.
    """

    result = agent.analyze(sample_report)

    print(result)
