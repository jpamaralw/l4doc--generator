from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from docxtpl import DocxTemplate
import os
import io
import zipfile
import sqlite3
from typing import Optional, List
from datetime import datetime, date

app = FastAPI(title="L4 Ativos - API de Documentos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("output", exist_ok=True)
os.makedirs("templates/branded", exist_ok=True)

DB_PATH = "l4docs.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT DEFAULT 'operador',
            cedente_nome TEXT,
            numero_processo TEXT,
            template_type TEXT DEFAULT 'padrao',
            data_geracao DATETIME DEFAULT CURRENT_TIMESTAMP,
            hora_geracao TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
def on_startup():
    init_db()

def save_historico(cedente_nome: str, numero_processo: str, template_type: str, usuario: str = "operador"):
    now = datetime.now()
    hora = now.strftime("%H:%M:%S")
    conn = get_db()
    conn.execute(
        "INSERT INTO historico (usuario, cedente_nome, numero_processo, template_type, data_geracao, hora_geracao) VALUES (?,?,?,?,?,?)",
        (usuario, cedente_nome, numero_processo, template_type, now.isoformat(), hora)
    )
    conn.commit()
    conn.close()

def format_currency(value):
    try:
        val = float(value)
        return f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return str(value) if value else ""

class AllDocumentsPayload(BaseModel):
    # Cedente
    nome_cedente: str
    cpf_cedente: str
    rg_cedente: str
    nacionalidade_cedente: str = "brasileiro(a)"
    profissao_cedente: str
    estado_civil_cedente: str
    endereco_cedente: str
    cep_cedente: str
    cidade_cedente: str = ""
    uf_cedente: str = ""
    data_nascimento: str

    # Cessionário
    nome_cessionario: str
    cpf_cessionario: str
    rg_cessionario: str
    nacionalidade_cessionario: str = "brasileira"
    profissao_cessionario: str
    estado_civil_cessionario: str
    endereco_cessionario: str
    cep_cessionario: str

    # Bancário
    banco: str = "Banco do Brasil"
    agencia: str
    conta: str
    pix: str = ""

    # Processo
    numero_processo: str
    numero_processo_origem: str
    devedor: str = "ESTADO DE GOIÁS"
    vara_unidade: str = "Unidade de Processamento Judicial dos Juizados Especiais da Fazenda Pública"
    comarca: str = "Goiânia"
    uf_comarca: str = "GO"

    # Financeiro
    valor_bruto: float
    valor_bruto_extenso: str = ""
    percentual_honorarios: float = 20.0
    valor_liquido: float
    valor_liquido_extenso: str = ""

    # Advogados
    nome_advogado: str = ""
    outorgado_nome_1: str = "DR. FÁBIO BATISTA BASTOS"
    outorgado_nacionalidade_1: str = "brasileiro"
    outorgado_estado_civil_1: str = "solteiro"
    outorgado_profissao_1: str = "advogado"
    outorgado_oab_1: str = "40.115"
    outorgado_nome_2: str = "DRA. NATANE ALINE DE CARVALHO MONTEIRO"
    outorgado_nacionalidade_2: str = "brasileira"
    outorgado_estado_civil_2: str = "solteira"
    outorgado_profissao_2: str = "advogada"
    outorgado_oab_2: str = "63.726"
    outorgado_cpf_2: str = "115.617.116-40"

    # Datas / Local
    local: str = "Brasília"
    data_contrato: str
    data_negociacao: str

    # Template
    template_type: str = "padrao"

    # Legacy compat
    @property
    def nome(self):
        return self.nome_cedente

@app.post("/api/generate-all")
async def generate_all(payload: AllDocumentsPayload):
    try:
        nome_limpo = payload.nome_cedente.replace(" ", "_")
        data_hoje = datetime.now().strftime("%Y%m%d")
        zip_filename = f"Documentos_{nome_limpo}_{data_hoje}.zip"

        use_branded = payload.template_type == "branded"
        if use_branded:
            templates_to_gen = [
                ("templates/branded/1_cessao-rpv-branded.docx", f"1_Contrato_Cessao_{nome_limpo}.docx"),
                ("templates/branded/2_procuracao-branded.docx", f"2_Procuracao_{nome_limpo}.docx"),
                ("templates/branded/3_ciencia-concordancia-branded.docx", f"3_Declaracao_Ciencia_{nome_limpo}.docx"),
                ("templates/branded/4_quitacao-branded.docx", f"4_Declaracao_Quitacao_{nome_limpo}.docx"),
            ]
        else:
            templates_to_gen = [
                ("templates/template-cessao-rpv.docx", f"1_Contrato_Cessao_{nome_limpo}.docx"),
                ("templates/template-procuracao-adjudicia.docx", f"2_Procuracao_{nome_limpo}.docx"),
                ("templates/template-dec-ciencia-concord.docx", f"3_Declaracao_Ciencia_{nome_limpo}.docx"),
                ("templates/template-dec-quitacao.docx", f"4_Declaracao_Quitacao_{nome_limpo}.docx"),
            ]

        ctx = {
            # Cedente
            "nome_cedente": payload.nome_cedente or "",
            "cpf_cedente": payload.cpf_cedente or "",
            "rg_cedente": payload.rg_cedente or "",
            "nacionalidade_cedente": payload.nacionalidade_cedente or "",
            "profissao_cedente": payload.profissao_cedente or "",
            "estado_civil_cedente": payload.estado_civil_cedente or "",
            "endereco_cedente": payload.endereco_cedente or "",
            "cep_cedente": payload.cep_cedente or "",
            "cidade_cedente": payload.cidade_cedente or "",
            "uf_cedente": payload.uf_cedente or "",
            "data_nascimento": payload.data_nascimento or "",

            # Cessionário
            "nome_cessionario": payload.nome_cessionario or "",
            "cpf_cessionario": payload.cpf_cessionario or "",
            "rg_cessionario": payload.rg_cessionario or "",
            "nacionalidade_cessionario": payload.nacionalidade_cessionario or "",
            "profissao_cessionario": payload.profissao_cessionario or "",
            "estado_civil_cessionario": payload.estado_civil_cessionario or "",
            "endereco_cessionario": payload.endereco_cessionario or "",
            "cep_cessionario": payload.cep_cessionario or "",

            # Bancário
            "banco": payload.banco or "",
            "agencia": payload.agencia or "",
            "conta": payload.conta or "",
            "pix": payload.pix or "",

            # Processo
            "numero_processo": payload.numero_processo or "",
            "numero_processo_origem": payload.numero_processo_origem or "",
            "devedor": payload.devedor or "",
            "vara_unidade": payload.vara_unidade or "",
            "comarca": payload.comarca or "",
            "uf_comarca": payload.uf_comarca or "",

            # Financeiro
            "valor_bruto": format_currency(payload.valor_bruto),
            "valor_bruto_extenso": payload.valor_bruto_extenso or "",
            "percentual_honorarios": f"{payload.percentual_honorarios:.2f}%",
            "valor_liquido": format_currency(payload.valor_liquido),
            "valor_liquido_extenso": payload.valor_liquido_extenso or "",

            # Advogados
            "nome_advogado": payload.nome_advogado or "",
            "outorgado_nome_1": payload.outorgado_nome_1 or "",
            "outorgado_nacionalidade_1": payload.outorgado_nacionalidade_1 or "",
            "outorgado_estado_civil_1": payload.outorgado_estado_civil_1 or "",
            "outorgado_profissao_1": payload.outorgado_profissao_1 or "",
            "outorgado_oab_1": payload.outorgado_oab_1 or "",
            "outorgado_nome_2": payload.outorgado_nome_2 or "",
            "outorgado_nacionalidade_2": payload.outorgado_nacionalidade_2 or "",
            "outorgado_estado_civil_2": payload.outorgado_estado_civil_2 or "",
            "outorgado_profissao_2": payload.outorgado_profissao_2 or "",
            "outorgado_oab_2": payload.outorgado_oab_2 or "",
            "outorgado_cpf_2": payload.outorgado_cpf_2 or "",

            # Datas / Local
            "local": payload.local or "",
            "data_contrato": payload.data_contrato or "",
            "data_negociacao": payload.data_negociacao or "",
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
            for t_path, out_name in templates_to_gen:
                if os.path.exists(t_path):
                    doc = DocxTemplate(t_path)
                    doc.render(ctx)
                    buf = io.BytesIO()
                    doc.save(buf)
                    zf.writestr(out_name, buf.getvalue())
                else:
                    print(f"WARNING: Template not found: {t_path}")

        zip_buffer.seek(0)
        save_historico(payload.nome_cedente, payload.numero_processo, payload.template_type)

        return StreamingResponse(
            zip_buffer,
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment; filename={zip_filename}"}
        )
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/historico")
def get_historico():
    conn = get_db()
    rows = conn.execute("SELECT * FROM historico ORDER BY data_geracao DESC LIMIT 500").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/historico/stats")
def get_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM historico").fetchone()[0]
    hoje = conn.execute(
        "SELECT COUNT(*) FROM historico WHERE date(data_geracao) = date('now', 'localtime')"
    ).fetchone()[0]
    cedentes_unicos = conn.execute("SELECT COUNT(DISTINCT cedente_nome) FROM historico").fetchone()[0]

    ultimos_7 = []
    rows = conn.execute("""
        SELECT date(data_geracao, 'localtime') as dia, COUNT(*) as total
        FROM historico
        WHERE data_geracao >= date('now', '-7 days', 'localtime')
        GROUP BY dia ORDER BY dia
    """).fetchall()
    for r in rows:
        ultimos_7.append({"dia": r[0], "total": r[1]})

    conn.close()
    return {
        "total": total,
        "hoje": hoje,
        "cedentes_unicos": cedentes_unicos,
        "ultimos_7_dias": ultimos_7
    }


app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.get("/curadoria")
def curadoria():
    return FileResponse("frontend/curadoria.html")

@app.get("/guia")
def guia():
    return FileResponse("frontend/guia.html")
