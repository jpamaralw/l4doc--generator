const isLocal =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1";

const API_URL = isLocal
  ? "http://127.0.0.1:8000"
  : "https://l4doc-api.onrender.com";

console.log(`🔗 Conectando à API: ${API_URL}`);

function switchTab(tabName) {
    const forms = document.querySelectorAll('.form-container');
    forms.forEach(form => form.classList.remove('active'));
    
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

async function gerarDocumento(tipo) {
    const forms = {
        'contrato': 'contratoForm',
        'procuracao': 'procuracaoForm',
        'ciencia': 'cienciaForm',
        'declaracao': 'declaracaoForm'
    };

    const form = document.getElementById(forms[tipo]);
    const formData = new FormData(form);
    const dados = Object.fromEntries(formData);

    if (!form.checkValidity()) {
        mostrarMensagem(tipo, 'Preencha todos os campos obrigatórios!', 'error');
        form.reportValidity();
        return;
    }

    mostrarMensagem(tipo, '⏳ Gerando documento...', 'success');

    try {
        const response = await fetch(`${API_URL}/gerar/${tipo}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Erro ao gerar documento');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${tipo}_${dados[Object.keys(dados)[0]].replace(/\s+/g, '_')}.docx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        mostrarMensagem(tipo, '✅ Documento gerado com sucesso!', 'success');
    } catch (error) {
        console.error('❌ Erro:', error);
        mostrarMensagem(tipo, `❌ ${error.message}`, 'error');
    }
}

function mostrarMensagem(tipo, mensagem, classe) {
    const msgDiv = document.getElementById(tipo + 'Msg');
    msgDiv.textContent = mensagem;
    msgDiv.className = 'message ' + classe;
    setTimeout(() => {
        if (classe === 'success' && !mensagem.includes('⏳')) {
            msgDiv.className = 'message';
        }
    }, 5000);
}