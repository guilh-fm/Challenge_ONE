import os
import glob
import re
from typing import List, Dict, Any, Tuple

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import criar_llm
from backend.prompts import obter_prompt_corporativo
from backend.document_loaders import carregar_arquivo_por_extensao

# Mapeamento de nomes de arquivo para títulos amigáveis corporativos
MAPA_TITULOS_DOCUMENTOS = {
    "manual_onboarding_santos_pegasus.pdf": "Manual de Onboarding - Cultura & Valores",
    "guia_engenharia_backend_santos_pegasus.pdf": "Guia Oficial de Engenharia Back-end (v3.0.0)",
    "guia_engenharia_frontend_santos_pegasus.pdf": "Guia Oficial de Engenharia Front-end (v2.0.0)",
    "protocolo_resposta_incidentes_sre_santos_pegasus.pdf": "Protocolo de Incidentes & Confiabilidade (SRE)",
    "arquitetura_microsservicos_mapa_dominios_santos_pegasus.pdf": "Arquitetura de Microsserviços & Domínios",
    "manual_colaborador_santos_pegasus.md": "Manual do Colaborador & Benefícios RH"
}

class RAGEngine:
    def __init__(self, pasta_documentos: str = "documentos"):
        self.pasta_documentos = pasta_documentos
        # Modelo de Embeddings Multilíngue otimizado para busca semântica em Português
        self.embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
        self.vector_store = None
        
        # Chunking otimizado com preservação de parágrafos
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=300,
            separators=["\n\n", "\n", ". ", " "]
        )
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
            print(f"[RAG Engine High-Perf] Indexados {len(chunks)} trechos de {len(self.documentos_indexados)} arquivos.")
        else:
            print("[RAG Engine High-Perf] Nenhum documento prévio encontrado na pasta 'documentos'.")

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
        print(f"[RAG Engine High-Perf] Adicionados {len(chunks)} trechos do arquivo '{nome_base}'.")
        return len(chunks)

    def obter_documentos_indexados(self) -> List[str]:
        return list(self.documentos_indexados)

    def expandir_consulta(self, pergunta: str) -> List[str]:
        """
        Técnica de Multi-Query Expansion: Gera variações da pergunta para capturar
        tanto palavras-chave exatas quanto a intenção semântica profunda.
        """
        consultas = [pergunta]
        palavras = [p.lower() for p in re.findall(r'\w+', pergunta) if len(p) > 2]
        
        # Se for pergunta sobre fundação / criação / história
        if any(w in pergunta.lower() for w in ['fundad', 'criad', 'nasc', 'histór', 'historia', 'inicio', 'início', 'origem', 'ano']):
            consultas.append("nossa historia nasceu em fundacao ano criadores vila madalena 2018 fundadores")
        
        # Se for sobre RH / Benefícios / Férias / Salário
        if any(w in pergunta.lower() for w in ['rh', 'benefic', 'benefíc', 'feria', 'férias', 'trabalh', 'salari', 'refeic', 'refeiç']):
            consultas.append("recursos humanos beneficios vr va flash plano de saude ferias CLT onboarding pessoas")
            
        # Se for sobre Engenharia / Arquitetura / Código / SRE
        if any(w in pergunta.lower() for w in ['backend', 'front', 'arquitet', 'microsserv', 'sre', 'incident', 'deploy', 'oci', 'java', 'docker']):
            consultas.append("engenharia de software microsservicos arquitetura gRPC kafka docker oci cloud aws sre plantao")

        if palavras:
            consultas.append(" ".join(palavras))

        return consultas

    def reordenar_e_filtrar_chunks(self, pergunta: str, docs_candidatos: List[Any], top_k: int = 6) -> List[Any]:
        """
        Técnica de Re-Ranking Semântico & Palavras-Chave (Hybrid Scoring):
        Avalia a relevância de cada trecho recuperado e seleciona os melhores sem duplicatas.
        """
        palavras_pergunta = set(re.findall(r'\w+', pergunta.lower()))
        scores = []
        vistos = set()

        for doc in docs_candidatos:
            conteudo = doc.page_content
            if conteudo in vistos:
                continue
            vistos.add(conteudo)

            conteudo_lower = conteudo.lower()
            palavras_conteudo = set(re.findall(r'\w+', conteudo_lower))
            
            # Cálculo de sobreposição de palavras-chave
            interseccao = palavras_pergunta.intersection(palavras_conteudo)
            overlap_score = len(interseccao) / (len(palavras_pergunta) + 1e-5)

            # Bônus para números/datas se a pergunta envolver números (ex: "ano", "quando", "quais")
            bonus_numero = 0
            if any(w in pergunta.lower() for w in ['ano', 'quando', 'quanto', 'data', 'valor']) and re.search(r'\b\d{4}\b|\b\d+\b', conteudo):
                bonus_numero = 0.5

            pontuacao_total = overlap_score + bonus_numero
            scores.append((pontuacao_total, doc))

        # Ordena do maior pro menor score
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scores[:top_k]]

    def responder_pergunta(self, pergunta: str, historico: List[Dict[str, str]] = None, modelo_llm: str = None) -> Dict[str, Any]:
        if self.vector_store is None:
            return {
                "resposta": "Nenhum documento foi indexado ainda. Por favor, adicione documentos na pasta 'documentos' ou via upload na interface.",
                "fontes": []
            }

        # Instancia o LLM do Groq com o modelo selecionado dinamicamente
        llm = criar_llm(modelo_especifico=modelo_llm)

        # 1. Multi-Query Expansion
        consultas = self.expandir_consulta(pergunta)

        # 2. Busca Multi-Vetorial no FAISS
        candidatos = []
        for q in consultas:
            res_q = self.vector_store.similarity_search(q, k=4)
            candidatos.extend(res_q)

        # 3. Hybrid Re-Ranking & Deduplicação
        docs_relevantes = self.reordenar_e_filtrar_chunks(pergunta, candidatos, top_k=6)

        # 4. Formata contexto e extrai fontes
        contexto_lista = []
        fontes = []
        fontes_vistas = set()
        
        for idx, doc in enumerate(docs_relevantes, start=1):
            meta = doc.metadata
            fonte_nome = meta.get("source", "Documento Interno")
            formato = meta.get("format", "")
            pagina = meta.get("page", meta.get("slide", meta.get("sheet", "")))
            
            detalhe_pagina = f" (Pág/Seção: {pagina})" if pagina != "" else ""
            contexto_lista.append(f"--- Trecho {idx} [{fonte_nome}{detalhe_pagina}] ---\n{doc.page_content}")
            
            chave_fonte = (fonte_nome, detalhe_pagina)
            if chave_fonte not in fontes_vistas:
                fontes_vistas.add(chave_fonte)
                titulo_amigavel = MAPA_TITULOS_DOCUMENTOS.get(fonte_nome, fonte_nome.replace("_", " ").replace(".pdf", "").title())
                fontes.append({
                    "arquivo": fonte_nome,
                    "titulo": titulo_amigavel,
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

        resposta_llm = llm.invoke(prompt_final)
        conteudo_resposta = resposta_llm.content if hasattr(resposta_llm, "content") else str(resposta_llm)

        return {
            "resposta": conteudo_resposta,
            "fontes": fontes
        }
