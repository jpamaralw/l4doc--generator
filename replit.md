# L4 Ativos - Gerador de Documentos Jurídicos

Automatic document generation system for legal contracts, powers of attorney, and declarations.

## Architecture

- **Backend + Frontend**: FastAPI (Python) serves both the API and the static HTML frontend on port 5000
- **Database**: SQLite (`l4docs.db`) via SQLModel, stores generated document records
- **Document generation**: `docxtpl` fills DOCX templates with user-submitted form data
- **Frontend**: Static HTML/CSS/JS in `frontend/` directory, served by FastAPI via `/static` mount

## Project Layout

```
app.py              # FastAPI backend + static file serving
requirements.txt    # Python dependencies
frontend/
  index.html        # Main UI (tabs for each document type)
  static/
    script.js       # API calls (uses relative URLs, same origin)
    styles.css      # Styling
    logo-l4.png     # Logo
    bg-map.gif      # Background animation
templates/          # DOCX template files
  template-cessao-rpv.docx
  template-dec-ciencia-concord.docx
  template-dec-quitacao.docx
  template-procuracao-adjudicia.docx
output/             # Generated documents (auto-created)
l4docs.db           # SQLite database (auto-created)
```

## Running

Workflow: `uvicorn app:app --host 0.0.0.0 --port 5000 --reload`

## API Endpoints

- `GET /` — Serves the frontend HTML
- `GET /static/*` — Serves static assets
- `POST /api/generate-all` — Generate all 4 documents in a single ZIP
- `GET /documentos` — List all generated documents

### Payload Example for `/api/generate-all`:
```json
{
  "nome": "João da Silva",
  "cpf": "123.456.789-00",
  "rg": "1234567-SSP/GO",
  "nacionalidade": "brasileiro(a)",
  "profissao": "Engenheiro",
  "estado_civil": "Casado(a)",
  "endereco": "Rua das Flores, 123",
  "cep": "74000-000",
  "data_nasc": "01/01/1980",
  "processo_numero": "0000000-00.2024.8.09.0001",
  "processo_devedor": "ESTADO DE GOIÁS",
  "processo_valor_bruto": 15000.00,
  "processo_valor_liquido": 12000.00,
  "processo_local": "Goiânia-GO",
  "processo_data": "02 de Março de 2026",
  "cessionario_nome": "L4 ATIVOS FINANCEIROS",
  "cessionario_cpf": "00.000.000/0001-00",
  "cessionario_rg": "Isento",
  "cessionario_profissao": "Empresa",
  "cessionario_endereco": "Av. Principal, 100",
  "cessionario_cep": "74000-001",
  "advogado_patrono": "Dr. Fulano de Tal",
  "banco": "Banco do Brasil",
  "agencia": "1234",
  "conta": "56789-0",
  "data_negociacao": "02/03/2026",
  "estado_devedor": "ESTADO DE GOIÁS",
  "unidade_judicial": "1ª Vara da Fazenda Pública",
  "comarca": "Goiânia",
  "processo_origem": "1234567-89.2023.8.09.0001"
}
```

## Key Notes

- Template files were renamed from their original GitHub names (with special chars/spaces) to clean names
- Frontend API calls use relative URLs (empty string base) so they work on any host
- SQLite is used by default; set `DATABASE_URL` env var to switch to PostgreSQL
