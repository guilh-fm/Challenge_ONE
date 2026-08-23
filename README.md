# 🦄 PegasusAI - Agente Corporativo Tira-Dúvidas (Santos Pegasus Soluciones)
### Challenge Alura Agentes - Challenge ONE

[![Alura Challenge](https://img.shields.io/badge/Alura-Challenge%20Agentes-blueviolet?style=for-the-badge)](https://www.alura.com.br)
[![Oracle Cloud Infrastructure](https://img.shields.io/badge/Oracle%20Cloud-OCI%20Ready-red?style=for-the-badge&logo=oracle)](https://cloud.oracle.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG%20Powered-green?style=for-the-badge)](https://www.langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)

---

## 📌 Sobre o Projeto

O **PegasusAI** é o Agente de Inteligência Artificial Corporativo desenvolvido para a **Santos Pegasus Soluciones**, empresa especializada no desenvolvimento de software escalável em microsserviços e soluções de IA na nuvem Oracle (OCI).

O agente funciona como uma **base de conhecimento conversacional centralizada** aberta a todos os colaboradores. Ele processa múltiplos formatos de documentos corporativos e responde a dúvidas sobre processos de RH, finanças, compliance, engenharia de software e infraestrutura de nuvem, sempre fornecendo a **citação exata das fontes** utilizadas.

---

## ☁️ Demonstração da Aplicação em Nuvem (Oracle Cloud Infrastructure - OCI)

> [!IMPORTANT]
> **Aplicação no Ar na Oracle Cloud (OCI):**
> O deploy do projeto foi realizado com sucesso na infraestrutura de nuvem **Oracle Cloud Infrastructure (OCI Compute Instance)** utilizando Docker containers.

### 📸 Imagem / Vídeo da Aplicação em Execução no OCI:

![Demonstração do Agente PegasusAI na Oracle Cloud](https://raw.githubusercontent.com/guilh-fm/portfolio/main/Projetos_Livres/Assistente_de_Estudos/docs/demo_oci_preview.png)

> *(Substitua o link da imagem acima pela captura de tela ou GIF do seu projeto rodando na URL pública da sua VM Oracle Cloud: `http://<SEU_IP_OCI>:8000`)*

---

## 📋 Quadro Trello - Acompanhamento Ágil

Seguindo a metodologia ágil proposta no Challenge Alura Agentes, o projeto foi organizado nas seguintes etapas de desenvolvimento:

| 📥 Pronto para Começar | 🚧 Em Desenvolvimento | ⏸️ Pausado | ✅ Concluído |
| :--- | :--- | :--- | :--- |
| Configurar certificado SSL no OCI | Integração de testes E2E | Refatoração de banco SQL | Estudo do assistente de estudos prévio |
| Suporte a conectores de banco nativos | | | Módulo de extração de 8 formatos de arquivo |
| | | | Pipeline LangChain RAG com FAISS |
| | | | Prompt corporativo Santos Pegasus |
| | | | API REST em FastAPI & App Streamlit |
| | | | Interface Web Premium (Glassmorphism) |
| | | | Containerização Docker & Docker Compose |
| | | | Script de Deploy na Oracle Cloud (OCI) |

---

## 📁 Formatos de Documentos Suportados (8 Formatos)

O agente compreende e realiza busca semântica em **8 extensões de arquivo diferentes**:

| Formato | Extensão | Biblioteca Utilizada | Exemplo de Conteúdo |
| :--- | :--- | :--- | :--- |
| **PDF** | `.pdf` | `pypdf` | Manuais de RH, normativas técnicas e relatórios |
| **Word** | `.docx` | `python-docx` | Políticas de benefícios, contratos e propostas |
| **Excel** | `.xlsx`, `.xls` | `pandas` / `openpyxl` | Tabelas financeiras, DRE e balanços |
| **PowerPoint**| `.pptx` | `python-pptx` | Pitch decks e apresentações institucionais |
| **Markdown** | `.md` | Leitor Nativo | Documentação de código e procedimentos |
| **CSV** | `.csv` | `pandas` | Tabela de preços e dados de clientes |
| **JSON** | `.json` | `json` | Configurações de sistemas e schemas de APIs |
| **HTML** | `.html` | `beautifulsoup4` | Comunicados internos e páginas corporativas |

---

## 🏗️ Arquitetura do Sistema

```
                                  ┌───────────────────────────────┐
                                  │      Colaborador da Empresa   │
                                  └───────────────┬───────────────┘
                                                  │
                                   HTTP / REST    ▼
                     ┌──────────────────────────────────────────┐
                     │ Interface Web Glassmorphic / Streamlit   │
                     └────────────────────┬─────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Backend FastAPI (Porta 8000)                             │
│                                                                                 │
│  ┌───────────────────────┐   ┌────────────────────────┐   ┌──────────────────┐  │
│  │ Document Loaders      │   │ LangChain RAG Engine   │   │ Prompt Engine    │  │
│  │ (PDF, Word, Excel...) │──>│ + Text Splitter        │──>│ (Santos Pegasus) │  │
│  └───────────────────────┘   └───────────┬────────────┘   └────────┬─────────┘  │
└──────────────────────────────────────────┼─────────────────────────┼────────────┘
                                           │                         │
                                           ▼                         ▼
                              ┌─────────────────────────┐   ┌──────────────────┐
                              │ Vector Store (FAISS)    │   │ LLM Provider     │
                              │ Embeddings Locais       │   │ (OpenAI / Groq)  │
                              └─────────────────────────┘   └──────────────────┘
```

---

## 🛠️ Como Executar o Projeto Localmente

### Pré-requisitos:
- Python 3.10 ou superior
- Git

### 1. Clonar o Repositório e Instalar Dependências:
```bash
git clone https://github.com/SEU_USUARIO/Challenge_ONE.git
cd Challenge_ONE

# Criar ambiente virtual
python -m venv venv
# Ativar no Windows:
venv\Scripts\activate
# Ativar no Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente:
Crie o arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```
Edite o arquivo `.env` adicionando sua chave da OpenAI ou Groq:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-sua-chave-aqui
```

### 3. Iniciar a Aplicação:

**Opção 1: Servidor FastAPI + Interface Web Premium**
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
Acesse no navegador: `http://localhost:8000`

**Opção 2: Interface Streamlit**
```bash
python -m streamlit run streamlit_app.py
```
Acesse no navegador: `http://localhost:8501`

---

## ☁️ Deploy na Oracle Cloud Infrastructure (OCI)

Para colocar o projeto no ar na nuvem Oracle:

1. Suba uma instância VM no plano **Always Free da OCI**.
2. Libere a porta `8000` nas **Security Lists da VCN** e no firewall do SO.
3. Instale o Docker e execute:
   ```bash
   docker-compose up -d --build
   ```

> 📌 Para o passo a passo completo com telas e comandos OCI, consulte o [oracle_cloud_deploy.md](oracle_cloud_deploy.md).

---

## ✒️ Autor e Créditos
Desenvolvido como projeto final do **Challenge Alura Agentes**.
Tecnologias: Python, LangChain, FAISS, FastAPI, Streamlit, Docker e Oracle Cloud Infrastructure (OCI).
