from typing import TypedDict


class DiagnosticState(TypedDict):

    case_id: str

    radiology_report: str
    pathology_report: str
    patient_history: str

    analyses: list
    conflicts: list
    debates: list
    consensus: dict