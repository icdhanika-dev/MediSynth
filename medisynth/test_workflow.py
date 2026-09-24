from workflow.diagnostic_workflow import build_workflow


workflow = build_workflow()


initial_state = {

    "case_id": "DEMO_CASE_001",

    "radiology_report": """
    Chest X-ray shows a focal opacity in the right lower lobe.
    No pleural effusion is seen.
    """,

    "pathology_report": """
    Histopathology shows chronic inflammatory cell infiltration.
    No malignant cells are identified.
    """,

    "patient_history": """
    Patient has fever and persistent cough for five days.
    Mild chest pain while breathing.
    """,

    "analyses": [],
    "conflicts": [],
    "debates": [],
    "consensus": {}
}


result = workflow.invoke(initial_state)


print("\n==============================")
print("SPECIALIST ANALYSES")
print("==============================")

for analysis in result["analyses"]:

    print("\nAgent:", analysis.agent)

    print("Findings:")
    for finding in analysis.findings:
        print("-", finding.finding)

    print("Possible conditions:")
    for condition in analysis.possible_conditions:
        print("-", condition)


print("\n==============================")
print("CONFLICTS")
print("==============================")

for conflict in result["conflicts"]:
    print(conflict)


print("\n==============================")
print("DEBATES")
print("==============================")

for debate in result["debates"]:
    print(debate)


print("\n==============================")
print("CONSENSUS")
print("==============================")

print(result["consensus"])


print("\n==============================")
print("WORKFLOW COMPLETE")
print("==============================")