# L4 Ativos — Gerador de Documentos Jurídicos

Sistema web para geração automatizada de documentos jurídicos de cessão de RPV (Requisição de Pequeno Valor). O operador preenche um único formulário e recebe um arquivo `.zip` com os 4 documentos prontos para assinatura.

## Documentos gerados

- Contrato de Cessão de Direitos Creditórios
- Procuração Ad Judicia
- Declaração de Ciência e Concordância
- Declaração de Quitação

## Stack

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.11 + FastAPI + docxtpl |
| Frontend | HTML / CSS / JS estático (sem framework) |
| Banco | SQLite — histórico de operações |
| Deploy API | [Render](https://render.com) |
| Deploy Frontend | [Netlify](https://netlify.com) |

## URLs de produção

| Serviço | URL |
|---------|-----|
| Frontend | https://l4-ativos-docs.netlify.app |
| API | https://l4doc-api.onrender.com |
| Painel de curadoria | https://l4-ativos-docs.netlify.app/curadoria |

## Como rodar localmente

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Suba o servidor
uvicorn app:app --reload --port 5000

# 3. Acesse
# http://localhost:5000
```

O frontend é servido diretamente pelo FastAPI em modo local. Em produção, o frontend fica no Netlify e chama a API no Render.

## Variáveis de ambiente

Nenhuma é obrigatória para rodar localmente.  
Em produção, configure no painel do Render conforme necessário.

## Acesso ao painel de curadoria

- **URL:** `/curadoria`
- **Senha:** solicitar à equipe L4 Ativos

O painel exibe data, hora, nome do cedente, número do processo e tipo de template de cada geração. Permite filtrar por período, nome e tipo de template, além de exportar CSV.

## Estrutura de pastas

```
l4doc--generator/
├── app.py                    # API FastAPI — endpoints e lógica de geração
├── requirements.txt          # Dependências Python
├── netlify.toml              # Configuração de deploy Netlify
├── frontend/
│   ├── index.html            # Formulário principal de geração
│   ├── curadoria.html        # Painel de histórico (protegido por senha)
│   ├── guia.html             # Manual de uso para a equipe
│   └── static/
│       ├── script.js         # Lógica JS — fetch, validação, máscaras
│       ├── styles.css        # Estilos globais
│       └── logo-l4.png       # Logotipo L4 Ativos
└── templates/
    ├── template-cessao-rpv.docx
    ├── template-procuracao.docx
    ├── template-declaracao-ciencia.docx
    ├── template-declaracao-quitacao.docx
    └── branded/              # Templates com cabeçalho e rodapé L4 Ativos
        ├── 1_cessao-rpv-branded.docx
        ├── 2_procuracao-branded.docx
        ├── 3_declaracao-ciencia-branded.docx
        └── 4_declaracao-quitacao-branded.docx
```

## Fluxo de geração

1. Operador preenche o formulário em `/`
2. Frontend envia `POST /api/generate-all` com todos os dados em JSON
3. Backend renderiza os 4 templates `.docx` via `docxtpl`
4. Retorna um `.zip` para download imediato
5. Registro é salvo no SQLite para consulta em `/curadoria`

## Tipos de template

| Tipo | Descrição |
|------|-----------|
| `padrao` | Template original sem identidade visual |
| `branded` | Template com cabeçalho e rodapé oficiais da L4 Ativos |
