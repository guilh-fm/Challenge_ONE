import os
import streamlit as st
from backend.rag_engine import RAGEngine

# Configuração da Página
st.set_page_config(
    page_title="Santos Pegasus AI - Agente Corporativo Groq",
    page_icon="🦄",
    layout="wide"
)

# Estilização Customizada CSS
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stAppHeader { background-color: transparent; }
    .stChatMessage { border-radius: 12px; margin-bottom: 12px; }
    .source-box { background: rgba(30, 41, 59, 0.7); border: 1px solid #3b82f6; border-radius: 8px; padding: 10px; margin-top: 5px; font-size: 0.85rem; }
    .empresa-title { font-size: 2rem; font-weight: 700; color: #60a5fa; margin-bottom: 0px; }
    .empresa-subtitle { font-size: 1rem; color: #94a3b8; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# Inicialização do RAG Engine na sessão do Streamlit
if "rag_engine" not in st.session_state:
    st.session_state["rag_engine"] = RAGEngine(pasta_documentos="documentos")

if "historico" not in st.session_state:
    st.session_state["historico"] = []

# Barra Lateral (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/unicorn.png", width=70)
    st.markdown("<div class='empresa-title'>Santos Pegasus</div>", unsafe_allow_html=True)
    st.markdown("<div class='empresa-subtitle'>Tira-Dúvidas Corporativo Groq</div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("⚙️ Provedor LLM Exclusivo")
    st.info("⚡ Modelo Ativo: Groq (`groq/compound-mini`)")
    os.environ["LLM_PROVIDER"] = "groq"

    st.divider()

    st.subheader("📁 Upload de Documentos")
    st.caption("Suporte: PDF, DOCX, XLSX, PPTX, MD, CSV, JSON, HTML")
    arquivos_enviados = st.file_uploader(
        "Carregar novo documento da empresa",
        type=["pdf", "docx", "xlsx", "pptx", "md", "csv", "json", "html"],
        accept_multiple_files=True
    )

    if arquivos_enviados:
        for arq in arquivos_enviados:
            caminho_temp = os.path.join("documentos", arq.name)
            with open(caminho_temp, "wb") as f:
                f.write(arq.getbuffer())
            chunks = st.session_state["rag_engine"].adicionar_documento(caminho_temp)
            st.success(f"'{arq.name}' indexado ({chunks} trechos)")

    st.divider()
    
    st.subheader("📚 Base de Conhecimento")
    docs_indexados = st.session_state["rag_engine"].obter_documentos_indexados()
    if docs_indexados:
        for doc in docs_indexados:
            st.caption(f"📄 {doc}")
    else:
        st.warning("Nenhum documento na base.")

# Área Principal
st.markdown("# 🦄 PegasusAI - Agente Corporativo (Groq Powered)")
st.markdown("Bem-vindo ao **PegasusAI**, seu assistente especialista na documentação interna da **Santos Pegasus Soluciones**. Respostas em altíssima velocidade impulsionadas pela **Groq**!")

st.divider()

# Exibe histórico de conversas
for msg in st.session_state["historico"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "fontes" in msg and msg["fontes"]:
            with st.expander("📚 Citação de Fontes"):
                for fonte in msg["fontes"]:
                    st.markdown(f"**Arquivo**: `{fonte['arquivo']}` {fonte['detalhe']}")
                    st.caption(f"Trecho: *{fonte['trecho']}*")

# Input do usuário
pergunta_usuario = st.chat_input("Digite sua dúvida sobre a empresa (ex: Quais são os benefícios do RH ou normas de OCI?)...")

if pergunta_usuario:
    # Exibe pergunta
    with st.chat_message("user"):
        st.write(pergunta_usuario)
    st.session_state["historico"].append({"role": "user", "content": pergunta_usuario})

    # Processa resposta
    with st.chat_message("assistant"):
        with st.spinner("Buscando na documentação da empresa via Groq..."):
            resultado = st.session_state["rag_engine"].responder_pergunta(
                pergunta=pergunta_usuario,
                historico=st.session_state["historico"]
            )
            resposta = resultado["resposta"]
            fontes = resultado["fontes"]
            
            st.write(resposta)
            
            if fontes:
                with st.expander("📚 Citação de Fontes"):
                    for fonte in fontes:
                        st.markdown(f"**Arquivo**: `{fonte['arquivo']}` {fonte['detalhe']}")
                        st.caption(f"Trecho: *{fonte['trecho']}*")

    st.session_state["historico"].append({
        "role": "assistant",
        "content": resposta,
        "fontes": fontes
    })
