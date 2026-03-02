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
- `GET /documentos` — List all generated documents
- `POST /gerar/contrato` — Generate cessão RPV contract
- `POST /gerar/procuracao` — Generate power of attorney
- `POST /gerar/ciencia` — Generate ciência e concordância declaration
- `POST /gerar/declaracao` — Generate quitação declaration

## Key Notes

- Template files were renamed from their original GitHub names (with special chars/spaces) to clean names
- Frontend API calls use relative URLs (empty string base) so they work on any host
- SQLite is used by default; set `DATABASE_URL` env var to switch to PostgreSQL
