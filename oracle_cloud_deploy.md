# ☁️ Guia de Deploy e Segurança de Chaves de API na Oracle Cloud Infrastructure (OCI)

Este guia orienta o passo a passo completo para realizar o deploy do **PegasusAI - Agente Corporativo da Santos Pegasus Soluciones** na **Oracle Cloud (OCI)** e como gerenciar as chaves de API (OpenAI / Groq) com total segurança.

---

## 🔒 Como Funciona o Gerenciamento Seguro de Chaves de API na OCI

> [!IMPORTANT]
> **Segurança em Primeiro Lugar:**
> A sua chave de API (`OPENAI_API_KEY` ou `GROQ_API_KEY`) **NUNCA deve ser commitada no GitHub público**.

Na Oracle Cloud, você possui 3 abordagens para fornecer as chaves de API à aplicação:

### Método 1: Arquivo `.env` Isolado na VM (Recomendado para o Challenge)
Quando você se conecta à sua VM da Oracle Cloud via SSH, o ambiente da nuvem funciona como o seu computador local, mas protegido pelo firewall da OCI.

1. Conecte-se à VM na Oracle Cloud:
   ```bash
   ssh -i /caminho/para/sua_chave.key ubuntu@<IP_PUBLICO_DA_VM>
   ```
2. Dentro da pasta do projeto na VM (`/home/ubuntu/Challenge_ONE`), crie o arquivo `.env`:
   ```bash
   nano .env
   ```
3. Insira suas chaves no arquivo `.env` da VM:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-sua-chave-real-da-openai-aqui
   GROQ_API_KEY=gsk_sua-chave-groq-aqui
   ```
4. Salve o arquivo (Ctrl+O, Enter, Ctrl+X).
5. Como o arquivo `.env` está configurado no `.gitignore`, ele nunca irá para o seu repositório no GitHub.
6. Ao executar `docker-compose up -d`, o Docker na VM Oracle lerá o arquivo `.env` local e injetará as chaves no container com total segurança.

---

### Método 2: Variáveis de Ambiente no Comando Docker Container
Caso prefira não gravar o arquivo `.env` em disco, você pode passar a chave diretamente ao rodar a imagem Docker na VM Oracle:

```bash
docker run -d \
  -p 8000:8000 \
  -e LLM_PROVIDER="openai" \
  -e OPENAI_API_KEY="sk-proj-sua-chave-real-da-openai-aqui" \
  -e GROQ_API_KEY="gsk_sua-chave-groq-aqui" \
  --name santos_pegasus_agent \
  santos-pegasus:latest
```

---

### Método 3: OCI Vault / Secrets Management (Padrão Corporativo)
Em ambientes corporativos da Santos Pegasus Soluciones na Oracle Cloud, utiliza-se o serviço **OCI Vault**:
1. No console da OCI, crie um **Vault** e uma **Secret** chamada `OPENAI_API_KEY`.
2. Conceda permissão à VM via **OCI IAM Instance Principal**.
3. O aplicativo busca o segredo em tempo de execução via SDK da Oracle (`oci.secrets.SecretsClient`).

---

## 💡 Dica Importante: Como Usar Chaves Gratuitas (Groq API)
Se você não deseja utilizar créditos pagos da OpenAI para testar o Challenge na Oracle Cloud, o **PegasusAI** possui integração nativa com a **Groq API**, que é **100% gratuita**:

1. Crie uma conta gratuita em [console.groq.com](https://console.groq.com/).
2. Gere uma API Key em *API Keys*.
3. No arquivo `.env` da sua VM na Oracle Cloud, defina:
   ```env
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_sua_chave_groq_gratuita
   ```
O agente passará a utilizar o modelo ultrarrápido **Llama 3.3 70B** sem custo!

---

## 🚀 Passo a Passo Completo do Deploy no OCI

### 1. Criar a VM na Oracle Cloud
1. No Console OCI, acesse **Compute** ➔ **Instances** ➔ **Create Instance**.
2. Escolha **Ubuntu 22.04 LTS**.
3. Escolha o Shape **VM.Standard.A1.Flex** (Always Free 4 OCPUs, 24GB RAM) ou **VM.Standard.E2.1.Micro**.
4. Baixe a chave SSH (`.key`) e clique em **Create**.

### 2. Liberação de Portas na OCI (Security List)
1. Clique na **Subnet** da VM ➔ **Default Security List**.
2. Adicione uma **Ingress Rule**:
   - Source: `0.0.0.0/0`
   - Protocol: `TCP`
   - Port Range: `8000`

### 3. Executar na VM Oracle
```bash
ssh -i sua_chave.key ubuntu@<IP_DA_VM>

# Instalar Docker
sudo apt-get update && sudo apt-get install -y docker.io docker-compose git
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# Liberar porta no firewall interno da VM
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT

# Clonar o repositório e criar o .env
git clone https://github.com/SEU_USUARIO/Challenge_ONE.git
cd Challenge_ONE
nano .env   # insira suas chaves aqui

# Iniciar aplicação
docker-compose up -d --build
```

Sua aplicação estará acessível em: `http://<IP_DA_VM>:8000`
