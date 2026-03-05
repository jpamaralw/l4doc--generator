const API_URL = "";

console.log(`🔗 Conectando à API: ${window.location.origin}`);

function switchTab(tabName) {
    const forms = document.querySelectorAll('.form-container');
    forms.forEach(form => form.classList.remove('active'));
    
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

async function generateAll() {
    const form = document.getElementById('generateAllForm');
    const formData = new FormData(form);
    const dados = Object.fromEntries(formData);

    // Formatar datas para DD/MM/AAAA
    const dateFields = ['data_nasc', 'processo_data', 'data_negociacao'];
    dateFields.forEach(field => {
        if (dados[field]) {
            const date = new Date(dados[field] + 'T12:00:00');
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const year = date.getFullYear();
            dados[field] = `${day}/${month}/${year}`;
        }
    });

    // Converter valores numéricos
    dados.processo_valor_bruto = parseFloat(dados.processo_valor_bruto) || 0;
    dados.processo_valor_liquido = parseFloat(dados.processo_valor_liquido) || 0;
    dados.percentual_honorarios = parseFloat(dados.percentual_honorarios) || 0;

    // Sincronizar patrono e outros campos ocultos
    dados.advogado_patrono = document.getElementById('lawyer1_nome').value;

    if (!form.checkValidity()) {
        mostrarMensagem('generate', 'Preencha todos os campos obrigatórios!', 'error');
        form.reportValidity();
        return;
    }

    mostrarMensagem('generate', '⏳ Gerando pacote de documentos...', 'success');

    try {
        const response = await fetch(`${API_URL}/api/generate-all`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Erro ao gerar documentos');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const nomeArquivo = `Documentos_${dados.nome.replace(/\s+/g, '_')}.zip`;
        a.download = nomeArquivo;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        mostrarMensagem('generate', '✅ 4 documentos gerados com sucesso!', 'success');
    } catch (error) {
        console.error('❌ Erro:', error);
        mostrarMensagem('generate', `❌ ${error.message}`, 'error');
    }
}

function resetLawyers() {
    document.getElementById('lawyer1_nome').value = "DR. FÁBIO BATISTA BASTOS";
    document.getElementById('lawyer1_oab').value = "40.115";
    document.getElementById('lawyer1_nacionalidade').value = "brasileiro";
    document.getElementById('lawyer1_estado_civil').value = "solteiro";
    document.getElementById('lawyer1_profissao').value = "advogado";

    document.getElementById('lawyer2_nome').value = "DRA. NATANE ALINE DE CARVALHO MONTEIRO";
    document.getElementById('lawyer2_oab').value = "63.726";
    document.getElementById('lawyer2_cpf').value = "115.617.116-40";
    document.getElementById('lawyer2_nacionalidade').value = "brasileira";
    document.getElementById('lawyer2_profissao').value = "advogada";
}

// Inicializar campos ao carregar
document.addEventListener('DOMContentLoaded', () => {
    resetLawyers();
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('input_data_contrato').value = hoje;
    document.getElementById('input_data_negociacao').value = hoje;
});

function mostrarMensagem(id, mensagem, classe) {
    const msgDiv = document.getElementById(id + 'Msg');
    msgDiv.textContent = mensagem;
    msgDiv.className = 'message ' + classe;
    setTimeout(() => {
        if (classe === 'success' && !mensagem.includes('⏳')) {
            msgDiv.className = 'message';
        }
    }, 5000);
}