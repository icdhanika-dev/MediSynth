from llm_client import call_llm


response = call_llm(
    "You are a medical AI assistant. "
    "Explain in one sentence what an X-ray is."
)

print("\nLLM RESPONSE:")
print(response)