import os
from dotenv import load_dotenv

load_dotenv()

PROVEDOR_LLM = os.getenv("LLM_PROVIDER", "groq").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Registry de Modelos Groq sem emojis
MODELOS_GROQ = {
    "openai/gpt-oss-120b": "GPT OSS 120B (Melhor Raciocínio & Síntese RAG)",
    "openai/gpt-oss-20b": "GPT OSS 20B (Veloz & Preciso)",
    "qwen/qwen3.6-27b": "Qwen 3.6 27B (Multilíngue Especialista)",
    "groq/compound-mini": "Groq Compound Mini (Resposta Instantânea)"
}
