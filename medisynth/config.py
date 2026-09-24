import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b:free"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

print("API KEY LOADED:", bool(OPENROUTER_API_KEY))
print("MODEL:", MODEL_NAME)

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "openai/gpt-oss-120b"

VISION_MODEL = "qwen/qwen3.8-27b"

print("GROQ KEY LOADED:", bool(GROQ_API_KEY))
print("GROQ MODEL:", GROQ_MODEL)