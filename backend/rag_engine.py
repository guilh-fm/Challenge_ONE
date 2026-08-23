import os
import glob
from typing import List, Dict, Any, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import criar_llm
from backend.prompts import obter_prompt_corporativo
from backend.document_loaders import carregar_arquivo_por_extensao

class RAGEngine:
    def __init__(self, pasta_documentos: str = "documentos"):
        self.pasta_documentos = pasta_documentos
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", " ", ""]
        )
        self.llm = None
        self.documentos_indexados = set()
        
        # Inicializa a base lendo os arquivos da pasta 'documentos'
        self.inicializar_base_conhecimento()

    def inicializar_base_conhecimento(self):
        documentos_todos = []
        
        if os.path.exists(self.pasta_documentos):
            arquivos = glob.glob(os.path.join(self.pasta_documentos, "*.*"))
            for arquivo in arquivos:
                docs = carregar_arquivo_por_extensao(arquivo)
                if docs:
                    documentos_todos.extend(docs)
                    self.documentos_indexados.add(os.path.basename(arquivo))

        if documentos_todos:
            chunks = self.text_splitter.split_documents(documentos_todos)
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            print(f"[RAG Engine] Indexados {len(chunks)} trechos de {len(self.documentos_indexados)} arquivos.")
        else:
            print("[RAG Engine] Nenhum documento prévio encontrado na pasta 'documentos'.")

    def adicionar_documento(self, caminho_arquivo: str) -> int:
        docs = carregar_arquivo_por_extensao(caminho_arquivo)
        if not docs:
            return 0

        chunks = self.text_splitter.split_documents(docs)
        if not chunks:
            return 0

        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vector_store.add_documents(chunks)

        nome_base = os.path.basename(caminho_arquivo)
        self.documentos_indexados.add(nome_base)
        print(f"[RAG Engine] Adicionados {len(chunks)} trechos do arquivo '{nome_base}'.")
        return len(chunks)

    def obter_documentos_indexados(self) -> List[str]:
        return list(self.documentos_indexados)

    def responder_pergunta(self, pergunta: str, historico: List[Dict[str, str]] = None) -> Dict[str, Any]:
        if self.vector_store is None:
            return {
                "resposta": "Nenhum documento foi indexado ainda. Por favor, adicione documentos na pasta 'documentos' ou via upload na interface.",
                "fontes": []
            }

        if self.llm is None:
            self.llm = criar_llm()

        # Busca os 4 trechos mais relevantes no FAISS
        docs_relevantes = self.vector_store.similarity_search(pergunta, k=4)

        # Formata o contexto e extrai as fontes
        contexto_lista = []
        fontes = []
        
        for idx, doc in enumerate(docs_relevantes, start=1):
            meta = doc.metadata
            fonte_nome = meta.get("source", "Documento Interno")
            formato = meta.get("format", "")
            pagina = meta.get("page", meta.get("slide", meta.get("sheet", "")))
            
            detalhe_pagina = f" (Pág/Seção: {pagina})" if pagina != "" else ""
            contexto_lista.append(f"--- Trecho {idx} [{fonte_nome}{detalhe_pagina}] ---\n{doc.page_content}")
            
            fontes.append({
                "arquivo": fonte_nome,
                "formato": formato,
                "detalhe": detalhe_pagina,
                "trecho": doc.page_content[:200] + "..."
            })

        contexto_str = "\n\n".join(contexto_lista)

        # Formata histórico recente
        chat_str = ""
        if historico:
            chat_str = "\n".join([f"{item.get('role', 'user')}: {item.get('content', '')}" for item in historico[-4:]])

        prompt = obter_prompt_corporativo()
        prompt_final = prompt.format(
            context=contexto_str,
            chat_history=chat_str,
            question=pergunta
        )

        resposta_llm = self.llm.invoke(prompt_final)
        conteudo_resposta = resposta_llm.content if hasattr(resposta_llm, "content") else str(resposta_llm)

        return {
            "resposta": conteudo_resposta,
            "fontes": fontes
        }
