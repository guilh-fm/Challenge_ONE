# Use uma imagem oficial Python leve
FROM python:3.11-slim

# Evita que o Python grave arquivos pyc e força buffer não retido de saída
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema operacional necessárias para compilações
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia dependências do projeto
COPY requirements.txt .

# Instala pacotes do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Cria pasta de documentos se não existir
RUN mkdir -p documentos

# Expõe a porta 8000 (FastAPI + Web UI)
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
