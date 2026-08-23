import os
from dotenv import load_dotenv

load_dotenv()

MODELO_GROQ_PADRAO = "groq/compound-mini"

def buscar_variavel(nome_variavel):
    valor = os.getenv(nome_variavel)
    if valor is None or valor.strip() == "":
        raise ValueError(f"A variável de ambiente '{nome_variavel}' não foi configurada.")
    return valor

def criar_llm(modelo="groq"):
    from langchain_groq import ChatGroq
    chave_groq = buscar_variavel("GROQ_API_KEY")
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", MODELO_GROQ_PADRAO),
        api_key=chave_groq,
        temperature=0.3,
    )

def formatar_historico(historico):
    texto = ""
    for mensagem in historico:
        papel = mensagem.get("role", "")
        conteudo = mensagem.get("content", "")
        texto += f"{papel}: {conteudo}\n"
    return texto
