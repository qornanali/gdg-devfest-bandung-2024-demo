import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SESSION_SECRET = os.getenv("SESSION_SECRET")
    SESSION_EXPIRATION = int(os.getenv("SESSION_EXPIRATION", "3600"))
    NODE_ENV = os.getenv("NODE_ENV", "development")
    PORT = int(os.getenv("PORT", "3000"))
    ORIGIN_URL = os.getenv("ORIGIN_URL")
    CREDENTIAL_TOKEN = os.getenv("CREDENTIAL_TOKEN")
    GEMINI_AI_BASE_URL = os.getenv("GEMINI_AI_BASE_URL")
    GEMINI_AI_MODEL_ID = os.getenv("GEMINI_AI_MODEL_ID")
    GEMINI_AI_API_KEY = os.getenv("GEMINI_AI_API_KEY")
    GEMINI_AI_TEMPERATURE = float(os.getenv("GEMINI_AI_TEMPERATURE", "0.2"))
    GEMINI_AI_MAX_OUTPUT_TOKENS = int(os.getenv("GEMINI_AI_MAX_OUTPUT_TOKENS", "100"))
    GEMINI_AI_TOP_P = float(os.getenv("GEMINI_AI_TOP_P", "0.8"))
    GEMINI_AI_TOP_K = int(os.getenv("GEMINI_AI_TOP_K", "3"))
