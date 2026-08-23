import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

MODELO_OPENAI_PADRAO = "gpt-4o-mini"
MODELO_GROQ_PADRAO = "llama-3.3-70b-versatile"

def buscar_variavel(nome_variavel: str, valor_padrao: str = None) -> str:
    valor = os.getenv(nome_variavel, valor_padrao)
    if not valor and valor_padrao is None:
        raise ValueError(f"A variável de ambiente '{nome_variavel}' não foi configurada.")
    return valor

def obter_provedor_llm() -> str:
    return os.getenv("LLM_PROVIDER", "openai").lower()

def criar_llm():
    provedor = obter_provedor_llm()
    
    if provedor == "openai":
        from langchain_openai import ChatOpenAI
        chave = buscar_variavel("OPENAI_API_KEY")
        modelo = os.getenv("OPENAI_MODEL", MODELO_OPENAI_PADRAO)
        return ChatOpenAI(
            model=modelo,
            api_key=chave,
            temperature=0.2
        )
    elif provedor == "groq":
        from langchain_groq import ChatGroq
        chave = buscar_variavel("GROQ_API_KEY")
        modelo = os.getenv("GROQ_MODEL", MODELO_GROQ_PADRAO)
        return ChatGroq(
            model=modelo,
            api_key=chave,
            temperature=0.2
        )
    else:
        raise ValueError(f"Provedor LLM '{provedor}' não suportado. Use 'openai' ou 'groq'.")
