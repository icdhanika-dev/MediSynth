class TreatmentAgent:
    def __init__(self):
        self.name = "Treatment Agent"

    def analyze(self, diagnosis):
        if not diagnosis:
            return {
                "agent": self.name,
                "finding": "No diagnosis provided",
                "treatment": "Unable to suggest treatment without diagnostic information",
                "confidence": 0.0
            }

        diagnosis_text = str(diagnosis).lower()

        treatment = "Further evaluation by a qualified medical professional is recommended."

        if "infection" in diagnosis_text:
            treatment = (
                "Treatment may involve appropriate antimicrobial therapy "
                "based on the confirmed infection and clinical evaluation."
            )

        elif "cancer" in diagnosis_text or "tumor" in diagnosis_text:
            treatment = (
                "Treatment may involve specialist oncology evaluation, "
                "follow-up imaging, surgery, radiation therapy, systemic therapy, "
                "or a combination depending on the confirmed diagnosis."
            )

        elif "fracture" in diagnosis_text:
            treatment = (
                "Treatment may involve immobilization, pain management, "
                "orthopedic evaluation, and follow-up imaging."
            )

        elif "inflammation" in diagnosis_text:
            treatment = (
                "Treatment depends on the underlying cause and may include "
                "medical evaluation, symptom management, and treatment of the cause."
            )

        return {
            "agent": self.name,
            "diagnosis": diagnosis,
            "treatment": treatment,
            "confidence": 0.85,
            "note": "This is decision-support information and not a substitute for professional medical advice."
        }
