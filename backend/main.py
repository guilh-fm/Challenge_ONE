import os
import shutil
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.rag_engine import RAGEngine, MAPA_TITULOS_DOCUMENTOS
from backend.config import MODELOS_GROQ

app = FastAPI(
    title="Santos Pegasus Soluciones - PegasusAI RAG API",
    description="API do Agente Tira-Dúvidas Corporativo para o Challenge Alura Agentes",
    version="1.0.0"
)

# Habilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o Engine RAG
rag_engine = RAGEngine(pasta_documentos="documentos")

class ChatRequest(BaseModel):
    pergunta: str
    historico: Optional[List[Dict[str, str]]] = []
    modelo_llm: Optional[str] = "openai/gpt-oss-120b"

@app.get("/api/health")
def health_check():
    # Detecta se a aplicação está rodando na Oracle Cloud (OCI) ou em Desenvolvimento Local
    is_oci = os.getenv("OCI_DEPLOYMENT", "").lower() in ["true", "1"] or os.path.exists("/.dockerenv")
    tipo_ambiente = "oci" if is_oci else "local"
    nome_ambiente = "Oracle Cloud Infrastructure (OCI)" if is_oci else "Ambiente Local (Desenvolvimento)"

    return {
        "status": "online",
        "empresa": "Santos Pegasus Soluciones",
        "agente": "PegasusAI RAG Specialist",
        "ambiente_tipo": tipo_ambiente,
        "ambiente_nome": nome_ambiente,
        "documentos_indexados": len(rag_engine.obter_documentos_indexados()),
        "modelos_disponiveis": MODELOS_GROQ
    }

@app.get("/api/documents")
def listar_documentos():
    arquivos = rag_engine.obter_documentos_indexados()
    documentos_formatados = []
    for arq in arquivos:
        titulo = MAPA_TITULOS_DOCUMENTOS.get(arq, arq.replace("_", " ").replace(".pdf", "").title())
        documentos_formatados.append({
            "arquivo": arq,
            "titulo": titulo
        })
    return {
        "documentos": documentos_formatados
    }

@app.get("/documentos/{filename}")
def obter_documento_pdf(filename: str):
    caminho_arquivo = os.path.join("documentos", filename)
    if os.path.exists(caminho_arquivo):
        return FileResponse(caminho_arquivo, media_type="application/pdf")
    raise HTTPException(status_code=404, detail="Documento não encontrado.")

@app.get("/api/models")
def listar_modelos():
    return {
        "modelos": MODELOS_GROQ
    }

@app.post("/api/chat")
def processar_chat(requisicao: ChatRequest):
    if not requisicao.pergunta.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    try:
        resultado = rag_engine.responder_pergunta(
            pergunta=requisicao.pergunta,
            historico=requisicao.historico,
            modelo_llm=requisicao.modelo_llm
        )
        return resultado
    except Exception as e:
        erro_str = str(e)
        if "insufficient_quota" in erro_str or "429" in erro_str:
            msg_erro = "⚠️ Erro de cota da API. Por favor, selecione outro modelo Groq na lista."
        elif "api_key" in erro_str.lower() or "not configured" in erro_str.lower():
            msg_erro = "⚠️ GROQ_API_KEY não encontrada. Configure a variável de ambiente."
        else:
            msg_erro = f"Erro na chamada da LLM Groq: {erro_str}"

        return {
            "resposta": msg_erro,
            "fontes": []
        }

@app.post("/api/upload")
async def carregar_documento(file: UploadFile = File(...)):
    pasta_destino = "documentos"
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_final = os.path.join(pasta_destino, file.filename)

    with open(caminho_final, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks_adicionados = rag_engine.adicionar_documento(caminho_final)

    return {
        "mensagem": f"Arquivo '{file.filename}' enviado e indexado com sucesso!",
        "arquivo": file.filename,
        "chunks_gerados": chunks_adicionados,
        "total_documentos": len(rag_engine.obter_documentos_indexados())
    }

# Monta o diretório do frontend se existir
caminho_frontend = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(caminho_frontend):
    app.mount("/", StaticFiles(directory=caminho_frontend, html=True), name="frontend")
