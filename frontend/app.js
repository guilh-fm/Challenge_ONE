const API_URL = window.location.origin;

document.addEventListener('DOMContentLoaded', () => {
    carregarDocumentos();

    // Upload Click & Drag-and-drop
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('fileInput');

    uploadBox.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fazerUploadArquivos(e.target.files);
        }
    });

    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = '#3b82f6';
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.style.borderColor = 'rgba(255, 255, 255, 0.1)';
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        if (e.dataTransfer.files.length > 0) {
            fazerUploadArquivos(e.dataTransfer.files);
        }
    });
});

async function carregarDocumentos() {
    const listEl = document.getElementById('documentList');
    try {
        const response = await fetch(`${API_URL}/api/documents`);
        const data = await response.json();
        
        if (data.documentos && data.documentos.length > 0) {
            listEl.innerHTML = data.documentos.map(doc => `
                <div class="doc-item">
                    <i class="fa-regular fa-file-lines"></i>
                    <span>${doc}</span>
                </div>
            `).join('');
        } else {
            listEl.innerHTML = '<p style="font-size:0.8rem; color:#6b7280;">Nenhum documento indexado.</p>';
        }
    } catch (err) {
        listEl.innerHTML = '<p style="font-size:0.8rem; color:#ef4444;">Erro ao carregar lista.</p>';
    }
}

async function fazerUploadArquivos(files) {
    const statusEl = document.getElementById('uploadStatus');
    statusEl.innerHTML = '<span style="color:#60a5fa;"><i class="fa-solid fa-spinner fa-spin"></i> Indexando...</span>';

    for (let file of files) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch(`${API_URL}/api/upload`, {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            statusEl.innerHTML = `<span style="color:#10b981;">✓ ${data.arquivo} indexado!</span>`;
        } catch (e) {
            statusEl.innerHTML = `<span style="color:#ef4444;">Erro no upload de ${file.name}</span>`;
        }
    }

    setTimeout(() => {
        statusEl.innerHTML = '';
        carregarDocumentos();
    }, 2500);
}

function usarPromptQuick(texto) {
    document.getElementById('userInput').value = texto;
    document.getElementById('sendBtn').click();
}

async function enviarMensagem(event) {
    event.preventDefault();
    const inputEl = document.getElementById('userInput');
    const pergunta = inputEl.value.trim();
    if (!pergunta) return;

    inputEl.value = '';

    // Adiciona mensagem do Usuário
    adicionarMensagemUI('user', pergunta);

    // Mensagem de aguardo
    const loadingId = adicionarMensagemLoading();

    try {
        const res = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pergunta: pergunta, historico: [] })
        });
        const data = await res.json();

        removerMensagem(loadingId);
        adicionarMensagemUI('assistant', data.resposta, data.fontes);

    } catch (e) {
        removerMensagem(loadingId);
        adicionarMensagemUI('assistant', 'Desculpe, ocorreu um erro ao se comunicar com o PegasusAI.');
    }
}

function adicionarMensagemUI(role, texto, fontes = []) {
    const chatContainer = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}-message`;

    const icon = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

    let fontesHTML = '';
    if (fontes && fontes.length > 0) {
        fontesHTML = `
            <div class="citations-wrapper">
                <div class="citation-title"><i class="fa-solid fa-quote-left"></i> Fontes Citadas:</div>
                ${fontes.map(f => `
                    <div class="citation-card">
                        <strong>📄 ${f.arquivo}</strong> ${f.detalhe}
                        <p style="color:#9ca3af; font-size:0.75rem; margin-top:2px;">"${f.trecho}"</p>
                    </div>
                `).join('')}
            </div>
        `;
    }

    msgDiv.innerHTML = `
        <div class="avatar">${icon}</div>
        <div class="message-content">
            <p>${texto.replace(/\n/g, '<br>')}</p>
            ${fontesHTML}
        </div>
    `;

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function adicionarMensagemLoading() {
    const chatContainer = document.getElementById('chatMessages');
    const id = 'loading-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message assistant-message';
    msgDiv.id = id;

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="message-content">
            <p><i class="fa-solid fa-circle-notch fa-spin"></i> Consultando a base da Santos Pegasus Soluciones...</p>
        </div>
    `;

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return id;
}

function removerMensagem(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}
