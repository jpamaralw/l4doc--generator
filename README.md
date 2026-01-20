# L4 Ativos - Gerador de Documentos Jurídicos

Sistema automático para geração de contratos, procurações e declarações.

## Estrutura

l4doc-generator/
├── frontend/index.html → Interface web
├── static/logo.jpg → Logo L4
├── templates/ → Templates Word (.docx)
├── app.py → Backend FastAPI
├── requirements.txt → Dependências
└── output/ → Documentos gerados

## Instalação Local

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
2. **Copiar Logo:**
# Copiar LogoL4ativos-Horizontal-02.jpg para static/logo.jpg
3. **Rodar backend:**
uvicorn app:app --reload --host 0.0.0.0 --port 8000
4. **Abrir Frontend:**
# Abrir frontend/index.html no navegador
# OU usar Live Server (VS Code)
