from agents.history_agent import analyze_history


history = """
The patient has had fever and persistent cough for five days.
The patient reports mild chest pain while breathing.
There is no known history of asthma or chronic lung disease.
"""


result = analyze_history(history)

print("\nPATIENT HISTORY AGENT TEST")
print(result.model_dump())