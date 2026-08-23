import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

MODELO_OPENAI_PADRAO = "gpt-4o-mini"
MODELO_GROQ_PADRAO = "groq/compound-mini"

def buscar_variavel(nome_variavel: str, valor_padrao: str = None) -> str:
    valor = os.getenv(nome_variavel, valor_padrao)
    if not valor and valor_padrao is None:
        raise ValueError(f"A variável de ambiente '{nome_variavel}' não foi configurada.")
    return valor

def obter_provedor_llm() -> str:
    provedor = os.getenv("LLM_PROVIDER")
    if provedor:
        return provedor.lower()
    
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    return "openai"

def criar_llm():
    provedor = obter_provedor_llm()
    chave_groq = os.getenv("GROQ_API_KEY")
    chave_openai = os.getenv("OPENAI_API_KEY")

    if provedor == "groq" or (not chave_openai and chave_groq):
        from langchain_groq import ChatGroq
        if not chave_groq or chave_groq.strip() == "":
            raise ValueError("GROQ_API_KEY não foi encontrada nas variáveis de ambiente.")
        
        modelo = os.getenv("GROQ_MODEL", MODELO_GROQ_PADRAO)
        print(f"[LLM Engine] Usando modelo Groq: {modelo}")
        return ChatGroq(
            model=modelo,
            api_key=chave_groq,
            temperature=0.2
        )

    # Padrão OpenAI
    from langchain_openai import ChatOpenAI
    if not chave_openai or chave_openai.strip() == "":
        if chave_groq:
            from langchain_groq import ChatGroq
            modelo = os.getenv("GROQ_MODEL", MODELO_GROQ_PADRAO)
            print(f"[LLM Engine] Fallback automático para Groq: {modelo}")
            return ChatGroq(
                model=modelo,
                api_key=chave_groq,
                temperature=0.2
            )
        raise ValueError("OPENAI_API_KEY não foi encontrada nas variáveis de ambiente.")

    modelo = os.getenv("OPENAI_MODEL", MODELO_OPENAI_PADRAO)
    print(f"[LLM Engine] Usando modelo OpenAI: {modelo}")
    return ChatOpenAI(
        model=modelo,
        api_key=chave_openai,
        temperature=0.2
    )
