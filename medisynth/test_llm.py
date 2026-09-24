from llm_client import call_llm

print("Testing Groq...")

result = call_llm("Reply with exactly: MediSynth works")

print("\nMODEL RESPONSE:")
print(result)
    