import os
from dotenv import load_dotenv

load_dotenv()

# Lista dos 4 melhores modelos de RAG da plataforma Groq
MODELOS_GROQ = {
    "openai/gpt-oss-120b": "GPT OSS 120B (🥇 Melhor Raciocínio & Síntese RAG)",
    "openai/gpt-oss-20b": "GPT OSS 20B (🥈 Veloz & Preciso)",
    "qwen/qwen3.6-27b": "Qwen 3.6 27B (🥉 Multilíngue Especialista)",
    "groq/compound-mini": "Groq Compound Mini (⚡ Resposta Instantânea)"
}

MODELO_GROQ_PADRAO = "openai/gpt-oss-120b"

def buscar_variavel(nome_variavel: str, valor_padrao: str = None) -> str:
    valor = os.getenv(nome_variavel, valor_padrao)
    if not valor and valor_padrao is None:
        raise ValueError(f"A variável de ambiente '{nome_variavel}' não foi configurada.")
    return valor

def criar_llm(modelo_especifico: str = None):
    """
    Cria a instância do modelo LLM Groq dinamicamente baseado na escolha do usuário.
    """
    from langchain_groq import ChatGroq
    
    chave_groq = os.getenv("GROQ_API_KEY")
    if not chave_groq or chave_groq.strip() == "":
        raise ValueError("A variável GROQ_API_KEY não foi encontrada nas variáveis de ambiente.")
    
    # Usa o modelo específico solicitado ou o padrão do ambiente
    modelo = modelo_especifico or os.getenv("GROQ_MODEL", MODELO_GROQ_PADRAO)
    print(f"[LLM Engine Groq] Instanciando modelo: {modelo}")
    
    return ChatGroq(
        model=modelo,
        api_key=chave_groq,
        temperature=0.2
    )
