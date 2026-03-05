# L4 Ativos — Gerador de Documentos Jurídicos

## Visão Geral
FastAPI backend + HTML/CSS/JS frontend para geração automática de 4 documentos jurídicos em formato .ZIP.

## Arquitetura
- **Backend**: FastAPI (Python), porta 5000
- **Frontend**: HTML/CSS/JS estático servido via FastAPI
- **Banco**: SQLite (`l4docs.db`) para histórico de gerações
- **Templates**: `docxtpl` (.docx com `{{variáveis}}`)

## Rotas Principais
| Rota | Descrição |
|------|-----------|
| `GET /` | Formulário principal (index.html) |
| `GET /curadoria` | Histórico protegido por senha |
| `GET /guia` | Guia de uso para a equipe |
| `POST /api/generate-all` | Gera ZIP com 4 documentos |
| `GET /api/historico` | Lista histórico de gerações |
| `GET /api/historico/stats` | Métricas (total, hoje, únicos) |

## Templates
- `templates/template-cessao-rpv.docx` — Contrato de Cessão RPV
- `templates/template-procuracao-adjudicia.docx` — Procuração Ad Judicia
- `templates/template-dec-ciencia-concord.docx` — Declaração de Ciência e Concordância
- `templates/template-dec-quitacao.docx` — Declaração de Quitação
- `templates/branded/` — Versões com logo L4 Ativos no cabeçalho e rodapé

## Variáveis de Template Utilizadas
**Cedente**: `nome_cedente`, `cpf_cedente`, `rg_cedente`, `nacionalidade_cedente`, `profissao_cedente`, `estado_civil_cedente`, `endereco_cedente`, `cep_cedente`, `cidade_cedente`, `uf_cedente`, `data_nascimento`

**Cessionário**: `nome_cessionario`, `cpf_cessionario`, `rg_cessionario`, `nacionalidade_cessionario`, `profissao_cessionario`, `estado_civil_cessionario`, `endereco_cessionario`, `cep_cessionario`

**Bancário**: `banco`, `agencia`, `conta`, `pix`

**Processo**: `numero_processo`, `numero_processo_origem`, `devedor`, `vara_unidade`, `comarca`, `uf_comarca`

**Financeiro**: `valor_bruto`, `valor_bruto_extenso`, `percentual_honorarios`, `valor_liquido`, `valor_liquido_extenso`

**Advogados**: `nome_advogado`, `outorgado_nome_1/2`, `outorgado_nacionalidade_1/2`, `outorgado_estado_civil_1/2`, `outorgado_profissao_1/2`, `outorgado_oab_1/2`, `outorgado_cpf_2`

**Datas/Local**: `data_contrato`, `data_negociacao`, `local`

## Senha da Curadoria
`l4admin2026`

## Dependências
- fastapi, uvicorn, docxtpl, python-docx, lxml, pydantic
