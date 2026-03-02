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

    // Converter valores numéricos
    dados.processo_valor_bruto = parseFloat(dados.processo_valor_bruto);
    dados.processo_valor_liquido = parseFloat(dados.processo_valor_liquido);

    if (!form.checkValidity()) {
        mostrarMensagem('generate', 'Preencha todos os campos obrigatórios!', 'error');
        form.reportValidity();
        return;
    }

    mostrarMensagem('generate', '⏳ Gerando pacote de documentos...', 'success');

    try {
        const response = await fetch(`${API_URL}/api/generate-all`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
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
        
        const dataAssinatura = dados.processo_data.replace(/\s+/g, '_').replace(/\//g, '-');
        a.download = `Documentos_${dados.nome.replace(/\s+/g, '_')}_${dataAssinatura}.zip`;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        mostrarMensagem('generate', '✅ Documentos gerados e baixados com sucesso!', 'success');
    } catch (error) {
        console.error('❌ Erro:', error);
        mostrarMensagem('generate', `❌ ${error.message}`, 'error');
    }
}

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