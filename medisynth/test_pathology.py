from agents.pathology_agent import analyze_pathology


report = """
Histopathology shows chronic inflammatory cell infiltration
with areas of tissue damage. No malignant cells are identified.
"""


result = analyze_pathology(report)

print("\nPATHOLOGY AGENT TEST")
print(result.model_dump())