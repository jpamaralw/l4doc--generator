import os
from docx import Document

def replace_text_in_paragraph(paragraph, old_text, new_text, occurrence=None, state={"count": 0}):
    if old_text not in paragraph.text:
        return False
    
    # We need to handle occurrences across the whole document for some tags
    # but since we process paragraph by paragraph, we'll use a global-ish state
    
    # Simple replacement if no specific occurrence is needed
    if occurrence is None:
        for run in paragraph.runs:
            if old_text in run.text:
                run.text = run.text.replace(old_text, new_text)
        return True
    
    # Handle specific occurrence
    # This is tricky because one [Tag] might be split across multiple runs
    # However, usually docxtpl placeholders are kept together or we assume simple case
    full_text = "".join(run.text for run in paragraph.runs)
    if old_text in full_text:
        # Check how many times it appeared before
        # For simplicity in this script, we'll do a basic version:
        # If the run contains the text, we check our global count
        for run in paragraph.runs:
            if old_text in run.text:
                state["count"] += 1
                if state["count"] == occurrence:
                    run.text = run.text.replace(old_text, new_text)
                    return True
    return False

def fix_ciencia_concord(doc):
    # Mapping for template-dec-ciencia-concord.docx
    # Note: filenames were renamed in previous turns
    state_nome = {"count": 0}
    state_nacionalidade = {"count": 0}
    state_profissao = {"count": 0}
    state_estado_civil = {"count": 0}
    state_rg = {"count": 0}
    state_cpf = {"count": 0}
    state_data = {"count": 0}
    state_endereco = {"count": 0}
    state_cep = {"count": 0}
    state_valor = {"count": 0}

    for p in doc.paragraphs:
        # CEDENTE
        replace_text_in_paragraph(p, "[Nome]", "{{nome_cedente}}", 1, state_nome)
        replace_text_in_paragraph(p, "[nacionalidade]", "{{nacionalidade_cedente}}", 1, state_nacionalidade)
        replace_text_in_paragraph(p, "[Profissão]", "{{profissao_cedente}}", 1, state_profissao)
        replace_text_in_paragraph(p, "[Estado Civil]", "{{estado_civil_cedente}}", 1, state_estado_civil)
        replace_text_in_paragraph(p, "[RG]", "{{rg_cedente}}", 1, state_rg)
        replace_text_in_paragraph(p, "[CPF]", "{{cpf_cedente}}", 1, state_cpf)
        replace_text_in_paragraph(p, "[Data]", "{{data_nascimento}}", 1, state_data)
        replace_text_in_paragraph(p, "[Endereço]", "{{endereco_cedente}}", 1, state_endereco)
        replace_text_in_paragraph(p, "[CEP]", "{{cep_cedente}}", 1, state_cep)
        
        # CESSIONÁRIO
        replace_text_in_paragraph(p, "[Nome]", "{{nome_cessionario}}", 2, state_nome)
        replace_text_in_paragraph(p, "[Profissão]", "{{profissao_cessionario}}", 2, state_profissao)
        replace_text_in_paragraph(p, "[Estado Civil]", "{{estado_civil_cessionario}}", 2, state_estado_civil)
        replace_text_in_paragraph(p, "[CPF]", "{{cpf_cessionario}}", 2, state_cpf)
        replace_text_in_paragraph(p, "[RG]", "{{rg_cessionario}}", 2, state_rg)
        replace_text_in_paragraph(p, "[Endereço]", "{{endereco_cessionario}}", 2, state_endereco)
        replace_text_in_paragraph(p, "[CEP]", "{{cep_cessionario}}", 2, state_cep)

        # Unique
        replace_text_in_paragraph(p, "[Número]", "{{numero_processo}}")
        replace_text_in_paragraph(p, "[Valor]", "{{valor_bruto}}", 1, state_valor)
        replace_text_in_paragraph(p, "[Valor]", "{{valor_liquido}}", 2, state_valor)
        replace_text_in_paragraph(p, "[Nome Advogado]", "{{nome_advogado}}")
        replace_text_in_paragraph(p, "[Agência]", "{{agencia}}")
        replace_text_in_paragraph(p, "[Conta]", "{{conta}}")
        replace_text_in_paragraph(p, "[Banco]", "{{banco}}")
        replace_text_in_paragraph(p, "[Nome Cedente]", "{{nome_cedente}}")

def fix_quitacao(doc):
    state_nome = {"count": 0}
    state_data = {"count": 0}
    for p in doc.paragraphs:
        replace_text_in_paragraph(p, "[Nome]", "{{nome_cedente}}", 1, state_nome)
        replace_text_in_paragraph(p, "[Nacionalidade]", "{{nacionalidade_cedente}}")
        replace_text_in_paragraph(p, "[Estado Civil]", "{{estado_civil_cedente}}")
        replace_text_in_paragraph(p, "[Profissão]", "{{profissao_cedente}}")
        replace_text_in_paragraph(p, "[RG]", "{{rg_cedente}}")
        replace_text_in_paragraph(p, "[CPF]", "{{cpf_cedente}}")
        replace_text_in_paragraph(p, "[Data]", "{{data_nascimento}}", 1, state_data)
        replace_text_in_paragraph(p, "[Endereço]", "{{endereco_cedente}}")
        replace_text_in_paragraph(p, "[CEP]", "{{cep_cedente}}")
        replace_text_in_paragraph(p, "[DD/MM/AAAA]", "{{data_negociacao}}")
        replace_text_in_paragraph(p, "[Número Processo]", "{{numero_processo}}")
        replace_text_in_paragraph(p, "[Vara/Unidade]", "{{vara_unidade}}")
        replace_text_in_paragraph(p, "[Comarca]", "{{comarca}}")
        replace_text_in_paragraph(p, "[Nome]", "{{nome_cedente}}", 2, state_nome)
        replace_text_in_paragraph(p, "[Número Processo Origem]", "{{numero_processo_origem}}")
        replace_text_in_paragraph(p, "[Local]", "{{local}}")
        replace_text_in_paragraph(p, "[Data]", "{{data_contrato}}", 2, state_data)

def fix_procuracao(doc):
    state_cpf = {"count": 0}
    state_data = {"count": 0}
    state_nome = {"count": 0}
    for p in doc.paragraphs:
        replace_text_in_paragraph(p, "[Nome]", "{{nome_cedente}}", 1, state_nome)
        replace_text_in_paragraph(p, "[Nacionalidade]", "{{nacionalidade_cedente}}")
        replace_text_in_paragraph(p, "[Estado Civil]", "{{estado_civil_cedente}}")
        replace_text_in_paragraph(p, "[Profissão]", "{{profissao_cedente}}")
        replace_text_in_paragraph(p, "[RG]", "{{rg_cedente}}")
        replace_text_in_paragraph(p, "[CPF]", "{{cpf_cedente}}", 1, state_cpf)
        replace_text_in_paragraph(p, "[Data Nasc]", "{{data_nascimento}}")
        replace_text_in_paragraph(p, "[Endereço]", "{{endereco_cedente}}")
        replace_text_in_paragraph(p, "[CEP]", "{{cep_cedente}}")
        
        # Hardcoded Outorgado
        replace_text_in_paragraph(p, "DR. FÁBIO BATISTA BASTOS", "{{outorgado_nome_1}}")
        replace_text_in_paragraph(p, "brasileiro, solteiro, advogado", "{{outorgado_nacionalidade_1}}, {{outorgado_estado_civil_1}}, {{outorgado_profissao_1}}")
        replace_text_in_paragraph(p, "sob o nº 40.115", "sob o nº {{outorgado_oab_1}}")
        replace_text_in_paragraph(p, "DRA. NATANE ALINE DE CARVALHO MONTEIRO", "{{outorgado_nome_2}}")
        replace_text_in_paragraph(p, "brasileira, advogada", "{{outorgado_nacionalidade_2}}, {{outorgado_profissao_2}}")
        replace_text_in_paragraph(p, "OAB/DF nº 63.726", "OAB/DF nº {{outorgado_oab_2}}")
        replace_text_in_paragraph(p, "CPF n°115.617.116-40", "CPF nº {{outorgado_cpf_2}}")
        
        replace_text_in_paragraph(p, "[Número Processo]", "{{numero_processo}}")
        replace_text_in_paragraph(p, "[Data]", "{{data_contrato}}", 2, state_data)
        replace_text_in_paragraph(p, "[Nome]", "{{nome_cedente}}", 2, state_nome)
        replace_text_in_paragraph(p, "[CPF]", "{{cpf_cedente}}", 2, state_cpf)

def fix_cessao(doc):
    old_block = "LEDA MARIA SOARES JANOT, brasileira, advogada, casada, portadora do CPF: 021.159.805-49 e RG nº 483293 SSP BA, residente a SMPW Q8 conjunto 3, casa 1, Park way, Brasília/DF, CEP: 71740-803"
    new_block = "{{nome_cessionario}}, {{nacionalidade_cessionario}}, {{profissao_cessionario}}, {{estado_civil_cessionario}}, portadora do CPF: {{cpf_cessionario}} e RG nº {{rg_cessionario}}, residente a {{endereco_cessionario}}, CEP: {{cep_cessionario}}"
    
    for p in doc.paragraphs:
        if old_block in p.text:
            replace_text_in_paragraph(p, old_block, new_block)
        replace_text_in_paragraph(p, "5314729-14.2025.8.09.0051", "{{numero_processo}}")
        replace_text_in_paragraph(p, "Devedor: Devedor:", "Devedor:")

templates = {
    "templates/template-dec-ciencia-concord.docx": fix_ciencia_concord,
    "templates/template-dec-quitacao.docx": fix_quitacao,
    "templates/template-procuracao-adjudicia.docx": fix_procuracao,
    "templates/template-cessao-rpv.docx": fix_cessao
}

for path, func in templates.items():
    if os.path.exists(path):
        doc = Document(path)
        func(doc)
        doc.save(path)
        print(f"Saved: {path}")
    else:
        print(f"Not found: {path}")

# Verification
for path in templates.keys():
    if os.path.exists(path):
        doc = Document(path)
        found = []
        for p in doc.paragraphs:
            if "[" in p.text or "]" in p.text:
                found.append(p.text)
        if found:
            print(f"Found remaining brackets in {path}:")
            for text in found:
                print(f"  - {text}")
        else:
            print(f"No brackets found in {path}")
