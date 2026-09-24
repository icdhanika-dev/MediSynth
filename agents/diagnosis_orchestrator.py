from patient_history_agent import PatientHistoryAgent
from pathology_agent import PathologyAgent
from radiology_agent import RadiologyAgent
from treatment_agent import TreatmentAgent


class DiagnosisOrchestrator:

    def __init__(self):
        self.name = "Diagnosis Orchestrator"

        self.patient_history_agent = PatientHistoryAgent()
        self.pathology_agent = PathologyAgent()
        self.radiology_agent = RadiologyAgent()
        self.treatment_agent = TreatmentAgent()

    def analyze(self, patient_history, pathology_report, radiology_report):

        # Step 1: Analyze patient history
        history_result = self.patient_history_agent.analyze(
            patient_history
        )

        # Step 2: Analyze pathology report
        pathology_result = self.pathology_agent.analyze(
            pathology_report
        )

        # Step 3: Analyze radiology report
        radiology_result = self.radiology_agent.analyze(
            radiology_report
        )

        # Step 4: Combine findings
        diagnosis = {
            "patient_history": history_result,
            "pathology": pathology_result,
            "radiology": radiology_result
        }

        # Step 5: Send combined diagnosis to treatment agent
        treatment_result = self.treatment_agent.analyze(
            diagnosis
        )

        # Step 6: Final result
        return {
            "agent": self.name,
            "diagnosis": diagnosis,
            "treatment": treatment_result
        }


# Example usage
if __name__ == "__main__":

    orchestrator = DiagnosisOrchestrator()

    result = orchestrator.analyze(
        patient_history="Patient has fever and persistent cough",
        pathology_report="No significant abnormality detected",
        radiology_report="Chest X-ray shows possible lung infection"
    )

    print(result)
