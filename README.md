# 🦄 PegasusAI - Agente Corporativo Tira-Dúvidas (Santos Pegasus Soluciones)
### Challenge Alura Agentes - Challenge ONE

[![Alura Challenge](https://img.shields.io/badge/Alura-Challenge%20Agentes-blueviolet?style=for-the-badge)](https://www.alura.com.br)
[![Oracle Cloud Infrastructure](https://img.shields.io/badge/Oracle%20Cloud-OCI%20Ready-red?style=for-the-badge&logo=oracle)](https://cloud.oracle.com)
[![Groq](https://img.shields.io/badge/Groq-API%20Powered-orange?style=for-the-badge)](https://console.groq.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG%20Powered-green?style=for-the-badge)](https://www.langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)

---

## 📌 Sobre o Projeto

O **PegasusAI** é o Agente de Inteligência Artificial Corporativo desenvolvido para a **Santos Pegasus Soluciones**, empresa especializada no desenvolvimento de software escalável em microsserviços e soluções de IA na nuvem Oracle (OCI).

O agente funciona como uma **base de conhecimento conversacional centralizada** aberta a todos os colaboradores. Ele processa múltiplos formatos de documentos corporativos e responde a dúvidas sobre processos de RH, finanças, compliance, engenharia de software e infraestrutura de nuvem, sempre fornecendo a **citação exata das fontes** utilizadas.

---

## ☁️ Evidência de Deploy na Nuvem (Oracle Cloud Infrastructure - OCI)

> [!IMPORTANT]
> **Aplicação no Ar na Oracle Cloud (OCI):**
> O deploy do projeto foi realizado na infraestrutura de nuvem **Oracle Cloud Infrastructure (OCI Compute Instance)** utilizando Docker containers.

### 📸 Captura de Tela / Vídeo da Aplicação em Execução no OCI:

![Demonstração do Agente PegasusAI na Oracle Cloud](https://raw.githubusercontent.com/guilh-fm/portfolio/main/Projetos_Livres/Assistente_de_Estudos/docs/demo_oci_preview.png)

> *(Link de Acesso OCI: `http://<IP_PUBLICO_DA_VM_ORACLE>:8000`)*

---

## ❓ Exemplos de Perguntas que o Agente Responde

O **PegasusAI** está preparado para responder a qualquer dúvida corporativa com base nos manuais e PDFs da empresa:

1. **História e Cultura**: *"Qual a história da Santos Pegasus Soluciones e quando foi fundada?"*
2. **RH e Benefícios**: *"Quais são os benefícios de RH oferecidos aos colaboradores CLT?"*
3. **Engenharia Back-end**: *"Quais são as diretrizes de testes automatizados e versão do Java no Back-end?"*
4. **Engenharia Front-end**: *"Quais são as regras de arquitetura para o desenvolvimento Front-end?"*
5. **Segurança e SRE**: *"Como funciona o protocolo de resposta a incidentes e o plantão On-Call da equipe SRE?"*
6. **Infraestrutura Cloud**: *"Quais são as diretrizes de segurança nas VCNs da Oracle Cloud (OCI)?"*

---

## 💬 Exemplos de Respostas Geradas pelo Agente

### Exemplo 1: Pergunta sobre Fundação da Empresa
> **Pergunta:** *"Foi fundada em qual ano?"*  
> **Resposta Gerada pelo PegasusAI:**  
> *"A **Santo Pegasus Soluciones** foi fundada no ano de **2018**, na garagem de um sobrado no bairro da Vila Madalena, em São Paulo, por três fundadores: uma engenheira de dados, um arquiteto de software e uma product designer."*  
> 📄 **Fonte Citada:** `manual_onboarding_santos_pegasus.pdf` *(Pág/Seção: 1)*

---

### Exemplo 2: Pergunta sobre Benefícios de Recursos Humanos
> **Pergunta:** *"Quais são os benefícios de RH da empresa?"*  
> **Resposta Gerada pelo PegasusAI:**  
> *"A Santos Pegasus Soluciones oferece um pacote completo de benefícios flexíveis para colaboradores CLT:*  
> - **Vale Refeição/Alimentação**: Cartão Flash flexível.  
> - **Plano de Saúde e Odontológico**: Bradesco Saúde Top Nacional sem co-participação para o titular.  
> - **Auxílio Home Office**: R$ 300 mensais para despesas de escritório em casa.  
> - **Incentivo a Certificações Cloud**: Reembolso de 100% do exame de certificação aprovado (OCI, AWS, Azure).  
> - **Gympass / Wellhub**: Cobertura nacional e global."*  
> 📄 **Fonte Citada:** `manual_colaborador_santos_pegasus.md`

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
                              │ Embeddings Multilíngue  │   │ (Groq Models)    │
                              └─────────────────────────┘   └──────────────────┘
```

---

## 🛠️ Como Executar o Projeto Localmente

### 1. Clonar o Repositório e Instalar Dependências:
```bash
git clone https://github.com/guilh-fm/Challenge_ONE.git
cd Challenge_ONE

# Criar e ativar ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente:
Crie o arquivo `.env`:
```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_sua_chave_groq_aqui
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
Desenvolvido por **Guilherme** para a **Santos Pegasus Soluciones** como projeto final do **Challenge Alura Agentes**.  
Tecnologias: Python, LangChain, FAISS, Groq API, FastAPI, Streamlit, Docker e Oracle Cloud Infrastructure (OCI).
