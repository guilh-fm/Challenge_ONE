import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

MODELO_GROQ_PADRAO = "groq/compound-mini"

def buscar_variavel(nome_variavel: str, valor_padrao: str = None) -> str:
    valor = os.getenv(nome_variavel, valor_padrao)
    if not valor and valor_padrao is None:
        raise ValueError(f"A variável de ambiente '{nome_variavel}' não foi configurada.")
    return valor

def obter_provedor_llm() -> str:
    # Provedor exclusivo Groq
    return "groq"

def criar_llm():
    """
    Cria a instância do modelo LLM configurado exclusivamente para a plataforma Groq.
    """
    from langchain_groq import ChatGroq
    
    chave_groq = os.getenv("GROQ_API_KEY")
    if not chave_groq or chave_groq.strip() == "":
        raise ValueError("A variável GROQ_API_KEY não foi encontrada nas variáveis de ambiente.")
    
    modelo = os.getenv("GROQ_MODEL", MODELO_GROQ_PADRAO)
    print(f"[LLM Engine Groq] Usando modelo exclusivo Groq: {modelo}")
    
    return ChatGroq(
        model=modelo,
        api_key=chave_groq,
        temperature=0.2
    )
