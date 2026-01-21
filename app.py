from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from docxtpl import DocxTemplate
import os
import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
import json

app = FastAPI(title="L4 Ativos - API de Documentos")

# CORS para permitir requests do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("output", exist_ok=True)

# ==== DATABASE CONFIG ==== #
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./l4docs.db")
engine = create_engine(DATABASE_URL, echo=False)

class Documento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo: str
    nome_principal: str
    payload_json: str
    arquivo_path: str
    criado_em: datetime = Field(default_factory=datetime.utcnow)

class DocumentoOut(BaseModel):
    id: int
    tipo: str
    nome_principal: str
    criado_em: datetime

    class Config:
        orm_mode = True

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def save_document(tipo: str, nome_principal: str, payload_dict: dict, arquivo_path: str):
    with Session(engine) as session:
        doc = Documento(
            tipo=tipo,
            nome_principal=nome_principal,
            payload_json=json.dumps(payload_dict, ensure_ascii=False),
            arquivo_path=arquivo_path,
        )
        session.add(doc)
        session.commit()

def format_currency(value):
    """Formata valor numérico para R$ com separadores corretos"""
    try:
        val = float(value)
        return f"R$ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return str(value)

# ==== MODELOS DE ENTRADA ==== #

class ContratoPayload(BaseModel):
    cedente_nome: str
    cedente_cpf: str
    cedente_rg: str
    cedente_nacionalidade: str
    cedente_profissao: str
    cedente_estado_civil: str
    cedente_endereco: str
    cedente_cep: str
    cedente_cidade: str
    cedente_uf: str
    processo_numero: str
    processo_devedor: str
    processo_valor_bruto: float
    processo_valor_liquido: float

class ProcuracaoPayload(BaseModel):
    outorgante_nome: str
    outorgante_cpf: str
    outorgante_rg: str
    outorgante_nacionalidade: str
    outorgante_profissao: str
    outorgante_estado_civil: str
    outorgante_endereco: str
    outorgante_cep: str
    outorgante_data_nasc: str
    proc_numero: str
    proc_local: str
    proc_data: str

class CienciaPayload(BaseModel):
    cedente2_nome: str
    cedente2_cpf: str
    cedente2_rg: str
    cedente2_nacionalidade: str
    cedente2_profissao: str
    cedente2_estado_civil: str
    cedente2_endereco: str
    cedente2_cep: str
    cedente2_data_nasc: str
    cessionario2_nome: str
    cessionario2_cpf: str
    cessionario2_rg: str
    cessionario2_profissao: str
    cessionario2_endereco: str
    cessionario2_cep: str
    proc2_numero: str
    proc2_valor_bruto: float
    proc2_valor_liquido: float
    proc2_advogado: str
    proc2_banco: str
    proc2_agencia: str
    proc2_conta: str
    proc2_data: str

class DeclaracaoPayload(BaseModel):
    decl_nome: str
    decl_cpf: str
    decl_rg: str
    decl_nacionalidade: str
    decl_profissao: str
    decl_estado_civil: str
    decl_endereco: str
    decl_cep: str
    decl_data_nasc: str
    decl_data_negociacao: str
    decl_processo: str
    decl_estado_devedor: str
    decl_unidade: str
    decl_comarca: str
    decl_processo_origem: str
    decl_local: str
    decl_data: str

# ==== ENDPOINTS ==== #

@app.get("/")
def root():
    return {"message": "L4 Ativos - API de Geração de Documentos"}

@app.get("/documentos", response_model=List[DocumentoOut])
def listar_documentos(limit: int = 50, offset: int = 0):
    """Lista todos os documentos gerados"""
    with Session(engine) as session:
        docs = (
            session.query(Documento)
            .order_by(Documento.criado_em.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return docs

@app.post("/gerar/contrato")
def gerar_contrato(payload: ContratoPayload):
    try:
        template_path = "templates/template-cessao-rpv.docx"
        doc = DocxTemplate(template_path)
        
        context = {
            "nome_cedente": payload.cedente_nome,
            "cpf_cedente": payload.cedente_cpf,
            "rg_cedente": payload.cedente_rg,
            "nacionalidade_cedente": payload.cedente_nacionalidade,
            "profissao_cedente": payload.cedente_profissao,
            "estado_civil_cedente": payload.cedente_estado_civil,
            "endereco_cedente": payload.cedente_endereco,
            "cep_cedente": payload.cedente_cep,
            "cidade_cedente": payload.cedente_cidade,
            "uf_cedente": payload.cedente_uf,
            "numero_processo": payload.processo_numero,
            "devedor": payload.processo_devedor,
            "valor_bruto": format_currency(payload.processo_valor_bruto),
            "valor_liquido": format_currency(payload.processo_valor_liquido),
        }
        
        doc.render(context)
        
        output_filename = f"output/contrato_{uuid.uuid4().hex[:8]}.docx"
        doc.save(output_filename)
        
        save_document(
            tipo="contrato",
            nome_principal=payload.cedente_nome,
            payload_dict=payload.dict(),
            arquivo_path=output_filename,
        )
        
        return FileResponse(
            output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"Contrato_{payload.cedente_nome.replace(' ', '_')}.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gerar/procuracao")
def gerar_procuracao(payload: ProcuracaoPayload):
    try:
        template_path = "templates/template-procuracao-adjudicia.docx"
        doc = DocxTemplate(template_path)
        
        context = {
            "Nome": payload.outorgante_nome,
            "Nacionalidade": payload.outorgante_nacionalidade,
            "Estado Civil": payload.outorgante_estado_civil,
            "Profissao": payload.outorgante_profissao,
            "RG": payload.outorgante_rg,
            "CPF": payload.outorgante_cpf,
            "Data Nasc": payload.outorgante_data_nasc,
            "Endereco": payload.outorgante_endereco,
            "CEP": payload.outorgante_cep,
            "Numero Processo": payload.proc_numero,
            "Local": payload.proc_local,
            "Data": payload.proc_data,
        }
        
        doc.render(context)
        
        output_filename = f"output/procuracao_{uuid.uuid4().hex[:8]}.docx"
        doc.save(output_filename)
        
        save_document(
            tipo="procuracao",
            nome_principal=payload.outorgante_nome,
            payload_dict=payload.dict(),
            arquivo_path=output_filename,
        )
        
        return FileResponse(
            output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"Procuracao_{payload.outorgante_nome.replace(' ', '_')}.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gerar/ciencia")
def gerar_ciencia(payload: CienciaPayload):
    try:
        template_path = "templates/template-dec-ciencia-concord.docx"
        doc = DocxTemplate(template_path)
        
        context = {
            "Nome": payload.cedente2_nome,
            "nacionalidade": payload.cedente2_nacionalidade,
            "Profissao": payload.cedente2_profissao,
            "Estado Civil": payload.cedente2_estado_civil,
            "RG": payload.cedente2_rg,
            "CPF": payload.cedente2_cpf,
            "Data": payload.cedente2_data_nasc,
            "Endereco": payload.cedente2_endereco,
            "CEP": payload.cedente2_cep,
            "Nome_Cessionario": payload.cessionario2_nome,
            "Profissao_Cessionario": payload.cessionario2_profissao,
            "CPF_Cessionario": payload.cessionario2_cpf,
            "RG_Cessionario": payload.cessionario2_rg,
            "Endereco_Cessionario": payload.cessionario2_endereco,
            "CEP_Cessionario": payload.cessionario2_cep,
            "Numero": payload.proc2_numero,
            "Valor_Bruto": format_currency(payload.proc2_valor_bruto),
            "Valor_Liquido": format_currency(payload.proc2_valor_liquido),
            "Nome Advogado": payload.proc2_advogado,
            "Agencia": payload.proc2_agencia,
            "Conta": payload.proc2_conta,
            "Banco": payload.proc2_banco,
            "Data_Final": payload.proc2_data,
        }
        
        doc.render(context)
        
        output_filename = f"output/ciencia_{uuid.uuid4().hex[:8]}.docx"
        doc.save(output_filename)
        
        save_document(
            tipo="ciencia",
            nome_principal=payload.cedente2_nome,
            payload_dict=payload.dict(),
            arquivo_path=output_filename,
        )
        
        return FileResponse(
            output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"Ciencia_{payload.cedente2_nome.replace(' ', '_')}.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gerar/declaracao")
def gerar_declaracao(payload: DeclaracaoPayload):
    try:
        template_path = "templates/template-dec-quitacao.docx"
        doc = DocxTemplate(template_path)
        
        context = {
            "Nome": payload.decl_nome,
            "Nacionalidade": payload.decl_nacionalidade,
            "Estado Civil": payload.decl_estado_civil,
            "Profissao": payload.decl_profissao,
            "RG": payload.decl_rg,
            "CPF": payload.decl_cpf,
            "Data": payload.decl_data_nasc,
            "Endereco": payload.decl_endereco,
            "CEP": payload.decl_cep,
            "DD/MM/AAAA": payload.decl_data_negociacao,
            "Numero Processo": payload.decl_processo,
            "Estado": payload.decl_estado_devedor,
            "Vara/Unidade": payload.decl_unidade,
            "Comarca": payload.decl_comarca,
            "Numero Processo Origem": payload.decl_processo_origem,
            "Local": payload.decl_local,
            "Data_Final": payload.decl_data,
        }
        
        doc.render(context)
        
        output_filename = f"output/declaracao_{uuid.uuid4().hex[:8]}.docx"
        doc.save(output_filename)
        
        save_document(
            tipo="declaracao_quitacao",
            nome_principal=payload.decl_nome,
            payload_dict=payload.dict(),
            arquivo_path=output_filename,
        )
        
        return FileResponse(
            output_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"Declaracao_{payload.decl_nome.replace(' ', '_')}.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
