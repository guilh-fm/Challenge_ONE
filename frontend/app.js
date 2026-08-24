const API_URL = window.location.origin;

document.addEventListener('DOMContentLoaded', () => {
    carregarDocumentos();
    verificarStatusAmbiente();
    inicializarTema();

    // Upload Click & Drag-and-drop
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('fileInput');

    if (uploadBox && fileInput) {
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
    }
});

async function verificarStatusAmbiente() {
    const statusTextEl = document.getElementById('statusText');
    const statusCardEl = document.getElementById('statusCard');
    const envBadgeEl = document.getElementById('envBadge');

    try {
        const response = await fetch(`${API_URL}/api/health`);
        const data = await response.json();

        const ehOCI = data.ambiente_tipo === 'oci';

        if (statusTextEl && statusCardEl) {
            if (ehOCI) {
                statusTextEl.innerHTML = 'Oracle Cloud (OCI): <strong>Online</strong>';
                statusCardEl.className = 'status-card status-oci';
            } else {
                statusTextEl.innerHTML = 'Ambiente Local (Dev): <strong>Online</strong>';
                statusCardEl.className = 'status-card status-local';
            }
        }

        if (envBadgeEl) {
            if (ehOCI) {
                envBadgeEl.className = 'badge badge-oci';
                envBadgeEl.innerHTML = '<i class="fa-solid fa-cloud"></i> Oracle Cloud (OCI)';
            } else {
                envBadgeEl.className = 'badge badge-local';
                envBadgeEl.innerHTML = '<i class="fa-solid fa-laptop-code"></i> Ambiente Local (Dev)';
            }
        }
    } catch (e) {
        if (statusTextEl) statusTextEl.innerHTML = 'Status: <strong>Offline</strong>';
    }
}

function inicializarTema() {
    const temaSalvo = localStorage.getItem('pegasus_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', temaSalvo);
}

function alternarTema() {
    const temaAtual = document.documentElement.getAttribute('data-theme') || 'dark';
    const novoTema = temaAtual === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', novoTema);
    localStorage.setItem('pegasus_theme', novoTema);
}

async function carregarDocumentos() {
    const listEl = document.getElementById('documentList');
    if (!listEl) return;
    try {
        const response = await fetch(`${API_URL}/api/documents`);
        const data = await response.json();
        
        if (data.documentos && data.documentos.length > 0) {
            listEl.innerHTML = data.documentos.map(doc => {
                const tituloFormatado = doc.titulo || doc.arquivo || doc;
                const nomeArquivo = doc.arquivo || doc;
                return `
                    <div class="doc-item" onclick="visualizarDocumento('${nomeArquivo}')" title="Clique para visualizar ${tituloFormatado}">
                        <i class="fa-solid fa-file-pdf"></i>
                        <span class="doc-title">${tituloFormatado}</span>
                        <i class="fa-solid fa-arrow-up-right-from-square doc-open-icon"></i>
                    </div>
                `;
            }).join('');
        } else {
            listEl.innerHTML = '<p style="font-size:0.8rem; color:#6b7280;">Nenhum documento indexado.</p>';
        }
    } catch (err) {
        listEl.innerHTML = '<p style="font-size:0.8rem; color:#ef4444;">Erro ao carregar lista.</p>';
    }
}

function visualizarDocumento(nomeArquivo) {
    window.open(`${API_URL}/documentos/${encodeURIComponent(nomeArquivo)}`, '_blank');
}

async function fazerUploadArquivos(files) {
    const statusEl = document.getElementById('uploadStatus');
    if (statusEl) statusEl.innerHTML = '<span style="color:#60a5fa;"><i class="fa-solid fa-spinner fa-spin"></i> Indexando...</span>';

    for (let file of files) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch(`${API_URL}/api/upload`, {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (statusEl) statusEl.innerHTML = `<span style="color:#10b981;">✓ ${data.arquivo} indexado!</span>`;
        } catch (e) {
            if (statusEl) statusEl.innerHTML = `<span style="color:#ef4444;">Erro no upload de ${file.name}</span>`;
        }
    }

    setTimeout(() => {
        if (statusEl) statusEl.innerHTML = '';
        carregarDocumentos();
    }, 2500);
}

function usarPromptQuick(texto) {
    const inputEl = document.getElementById('userInput');
    if (inputEl) {
        inputEl.value = texto;
        const sendBtn = document.getElementById('sendBtn');
        if (sendBtn) sendBtn.click();
    }
}

async function enviarMensagem(event) {
    event.preventDefault();
    const inputEl = document.getElementById('userInput');
    const modelSelectEl = document.getElementById('modelSelect');

    const pergunta = inputEl ? inputEl.value.trim() : '';
    const modeloSelecionado = modelSelectEl ? modelSelectEl.value : 'openai/gpt-oss-120b';

    if (!pergunta) return;

    if (inputEl) inputEl.value = '';

    // Adiciona mensagem do Usuário
    adicionarMensagemUI('user', pergunta);

    // Mensagem de aguardo
    const loadingId = adicionarMensagemLoading();

    try {
        const res = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                pergunta: pergunta,
                historico: [],
                modelo_llm: modeloSelecionado
            })
        });
        const data = await res.json();

        removerMensagem(loadingId);
        adicionarMensagemUI('assistant', data.resposta, data.fontes);

    } catch (e) {
        removerMensagem(loadingId);
        adicionarMensagemUI('assistant', 'Desculpe, ocorreu um erro ao se comunicar com o PegasusAI.');
    }
}

function renderizarMarkdown(texto) {
    if (!texto) return '';

    // Converte sintaxe de colchetes de fórmulas [ ... ] para KaTeX explicito $$ ... $$
    let textoProcessado = texto.replace(/\[\s*([\s\S]*?(?:\\frac|\\cdot|_|\^|=|\\boxed)[\s\S]*?)\s*\]/g, '\n\n$$$$ $1 $$$$\n\n');

    if (typeof marked !== 'undefined' && marked.parse) {
        return marked.parse(textoProcessado);
    }
    return textoProcessado.replace(/\n/g, '<br>');
}

function alternarFontes(btnEl) {
    const parent = btnEl.closest('.message-content');
    if (!parent) return;
    const sourcesWrapper = parent.querySelector('.citations-popover');
    if (sourcesWrapper) {
        const estaVisivel = sourcesWrapper.style.display === 'block';
        sourcesWrapper.style.display = estaVisivel ? 'none' : 'block';
        btnEl.classList.toggle('ativo', !estaVisivel);
    }
}

function adicionarMensagemUI(role, texto, fontes = []) {
    const chatContainer = document.getElementById('chatMessages');
    if (!chatContainer) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}-message`;

    const icon = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

    let fontesHTML = '';
    if (role === 'assistant' && fontes && fontes.length > 0) {
        fontesHTML = `
            <div class="citations-action-bar">
                <button class="btn-ver-fontes" onclick="alternarFontes(this)">
                    <i class="fa-solid fa-book-bookmark"></i> Ver Fontes Citadas (${fontes.length})
                </button>
                <div class="citations-popover" style="display: none;">
                    <div class="citation-popover-header">
                        <span><i class="fa-solid fa-quote-left"></i> Fontes Consultadas</span>
                    </div>
                    ${fontes.map(f => `
                        <div class="citation-card" onclick="visualizarDocumento('${f.arquivo}')" style="cursor:pointer;" title="Clique para abrir ${f.arquivo}">
                            <strong>📄 ${f.titulo || f.arquivo}</strong> ${f.detalhe}
                            <p style="color:#9ca3af; font-size:0.75rem; margin-top:2px;">"${f.trecho}"</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    const conteudoHTML = role === 'assistant' ? renderizarMarkdown(texto) : `<p>${texto.replace(/\n/g, '<br>')}</p>`;

    msgDiv.innerHTML = `
        <div class="avatar">${icon}</div>
        <div class="message-content">
            <div class="markdown-body">${conteudoHTML}</div>
            ${fontesHTML}
        </div>
    `;

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Renderiza Fórmulas Matemáticas via KaTeX se houver
    if (role === 'assistant' && typeof renderMathInElement !== 'undefined') {
        try {
            renderMathInElement(msgDiv, {
                delimiters: [
                    {left: '$$', right: '$$', display: true},
                    {left: '$', right: '$', display: false},
                    {left: '\\[', right: '\\]', display: true},
                    {left: '\\(', right: '\\)', display: false},
                    {left: '[', right: ']', display: true}
                ],
                ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
                throwOnError: false
            });
        } catch (e) {
            console.warn('Erro ao renderizar KaTeX:', e);
        }
    }
}

function adicionarMensagemLoading() {
    const chatContainer = document.getElementById('chatMessages');
    if (!chatContainer) return null;

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
    if (!id) return;
    const el = document.getElementById(id);
    if (el) el.remove();
}
