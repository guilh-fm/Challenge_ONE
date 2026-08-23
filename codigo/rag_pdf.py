from backend.document_loaders import carregar_arquivo_por_extensao
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

def carregar_e_processar_documento(caminho_arquivo):
    documentos = carregar_arquivo_por_extensao(caminho_arquivo)
    if not documentos:
        return None
    
    divisor = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = divisor.split_documents(documentos)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store
