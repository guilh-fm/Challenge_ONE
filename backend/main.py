import os
import shutil
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.rag_engine import RAGEngine

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

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "empresa": "Santos Pegasus Soluciones",
        "agente": "PegasusAI RAG Specialist",
        "documentos_indexados": len(rag_engine.obter_documentos_indexados())
    }

@app.get("/api/documents")
def listar_documentos():
    return {
        "documentos": rag_engine.obter_documentos_indexados()
    }

@app.post("/api/chat")
def processar_chat(requisicao: ChatRequest):
    if not requisicao.pergunta.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    resultado = rag_engine.responder_pergunta(
        pergunta=requisicao.pergunta,
        historico=requisicao.historico
    )
    return resultado

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
