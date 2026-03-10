const API_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:5000"
  : "https://l4doc-api.onrender.com";

function showToast(msg, type = "success") {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = `toast ${type}`;
  void t.offsetWidth;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 5000);
}

function formatDate(iso) {
  if (!iso) return "";
  const [y, m, d] = iso.split("-");
  return `${d}/${m}/${y}`;
}

function setDefaultDates() {
  const today = new Date().toISOString().split("T")[0];
  const dc = document.getElementById("data_contrato");
  const dn = document.getElementById("data_negociacao");
  if (dc && !dc.value) dc.value = today;
  if (dn && !dn.value) dn.value = today;
}

function resetLawyers() {
  const set = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };
  set("outorgado_nome_1", "DR. FÁBIO BATISTA BASTOS");
  set("outorgado_nacionalidade_1", "brasileiro");
  set("outorgado_estado_civil_1", "solteiro");
  set("outorgado_profissao_1", "advogado");
  set("outorgado_oab_1", "40.115");
  set("outorgado_nome_2", "DRA. NATANE ALINE DE CARVALHO MONTEIRO");
  set("outorgado_nacionalidade_2", "brasileira");
  set("outorgado_estado_civil_2", "solteira");
  set("outorgado_profissao_2", "advogada");
  set("outorgado_oab_2", "63.726");
  set("outorgado_cpf_2", "115.617.116-40");
}

function updateTemplateOpt() {
  const padrao = document.getElementById("opt_padrao");
  const branded = document.getElementById("opt_branded");
  const brandedNotice = document.getElementById("branded_notice");
  if (!padrao || !branded) return;
  const val = document.querySelector('input[name="template_type"]:checked')?.value;
  padrao.classList.toggle("selected", val === "padrao");
  branded.classList.toggle("selected", val === "branded");
  if (brandedNotice) brandedNotice.style.display = val === "branded" ? "block" : "none";
}

function calcLiquido() {
  const bruto = parseFloat(document.getElementById("valor_bruto")?.value) || 0;
  const pct = parseFloat(document.getElementById("percentual_honorarios")?.value) || 0;
  const liquido = bruto - (bruto * pct / 100);
  const elL = document.getElementById("valor_liquido");
  if (elL && bruto > 0) elL.value = liquido.toFixed(2);
}

function maskCPF(el) {
  let v = el.value.replace(/\D/g, "").substring(0, 11);
  v = v.replace(/(\d{3})(\d)/, "$1.$2")
       .replace(/(\d{3})\.(\d{3})(\d)/, "$1.$2.$3")
       .replace(/(\d{3})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3-$4");
  el.value = v;
}

function maskCEP(el) {
  let v = el.value.replace(/\D/g, "").substring(0, 8);
  v = v.replace(/(\d{5})(\d)/, "$1-$2");
  el.value = v;
}

function isValidCPF(val) {
  return /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(val);
}

function isValidCEP(val) {
  return /^\d{5}-\d{3}$/.test(val);
}

function showFieldError(el, msg) {
  el.classList.add("invalid");
  el.title = msg;
}

function getFormData() {
  const form = document.getElementById("mainForm");
  const data = {};
  const inputs = form.querySelectorAll("input, select, textarea");
  inputs.forEach(el => {
    if (el.name) data[el.name] = el.value;
  });
  return data;
}

function validateForm(data) {
  const required = [
    "nome_cedente","cpf_cedente","rg_cedente","nacionalidade_cedente","profissao_cedente",
    "estado_civil_cedente","data_nascimento","endereco_cedente","cep_cedente",
    "banco","agencia","conta",
    "nome_cessionario","cpf_cessionario","rg_cessionario","nacionalidade_cessionario",
    "profissao_cessionario","estado_civil_cessionario","endereco_cessionario","cep_cessionario",
    "numero_processo","numero_processo_origem","devedor","uf_comarca","comarca","vara_unidade",
    "valor_bruto","valor_bruto_extenso","valor_liquido","valor_liquido_extenso",
    "outorgado_nome_1","outorgado_nome_2",
    "local","data_contrato","data_negociacao"
  ];
  let valid = true;
  document.querySelectorAll(".invalid").forEach(el => {
    el.classList.remove("invalid");
    el.title = "";
  });

  required.forEach(name => {
    const el = document.getElementById(name);
    if (el && !el.value.trim()) {
      showFieldError(el, "Campo obrigatório");
      valid = false;
    }
  });

  const cpfCedente = document.getElementById("cpf_cedente");
  if (cpfCedente && cpfCedente.value && !isValidCPF(cpfCedente.value)) {
    showFieldError(cpfCedente, "CPF inválido — use o formato 000.000.000-00");
    valid = false;
  }

  const cpfCessionario = document.getElementById("cpf_cessionario");
  if (cpfCessionario && cpfCessionario.value && !isValidCPF(cpfCessionario.value)) {
    showFieldError(cpfCessionario, "CPF inválido — use o formato 000.000.000-00");
    valid = false;
  }

  const cepCedente = document.getElementById("cep_cedente");
  if (cepCedente && cepCedente.value && !isValidCEP(cepCedente.value)) {
    showFieldError(cepCedente, "CEP inválido — use o formato 00000-000");
    valid = false;
  }

  const cepCessionario = document.getElementById("cep_cessionario");
  if (cepCessionario && cepCessionario.value && !isValidCEP(cepCessionario.value)) {
    showFieldError(cepCessionario, "CEP inválido — use o formato 00000-000");
    valid = false;
  }

  const proc = document.getElementById("numero_processo");
  if (proc && proc.value && !/^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$/.test(proc.value)) {
    showFieldError(proc, "Formato esperado: 0000000-00.0000.0.00.0000");
    valid = false;
  }

  const vb = document.getElementById("valor_bruto");
  if (vb && (isNaN(parseFloat(vb.value)) || parseFloat(vb.value) <= 0)) {
    showFieldError(vb, "Informe um valor bruto maior que zero");
    valid = false;
  }

  const vl = document.getElementById("valor_liquido");
  if (vl && (isNaN(parseFloat(vl.value)) || parseFloat(vl.value) <= 0)) {
    showFieldError(vl, "Informe um valor líquido maior que zero");
    valid = false;
  }

  return valid;
}

document.addEventListener("DOMContentLoaded", () => {
  resetLawyers();
  setDefaultDates();

  ["cpf_cedente","cpf_cessionario","outorgado_cpf_2"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", () => maskCPF(el));
  });

  ["cep_cedente","cep_cessionario"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", () => maskCEP(el));
  });

  const vb = document.getElementById("valor_bruto");
  const pct = document.getElementById("percentual_honorarios");
  if (vb) vb.addEventListener("input", calcLiquido);
  if (pct) pct.addEventListener("input", calcLiquido);

  const form = document.getElementById("mainForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      await generateAll();
    });
  }
});

async function generateAll() {
  const data = getFormData();

  if (!validateForm(data)) {
    showToast("❌ Corrija os campos destacados em vermelho antes de continuar.", "error");
    const first = document.querySelector(".invalid");
    if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }

  data.data_nascimento = formatDate(data.data_nascimento);
  data.data_contrato = formatDate(data.data_contrato);
  data.data_negociacao = formatDate(data.data_negociacao);

  data.valor_bruto = parseFloat(data.valor_bruto) || 0;
  data.valor_liquido = parseFloat(data.valor_liquido) || 0;
  data.percentual_honorarios = parseFloat(data.percentual_honorarios) || 0;

  const btn = document.getElementById("btnGerar");
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Gerando documentos...';

  try {
    const response = await fetch(`${API_URL}/api/generate-all`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      let detail = "Erro desconhecido";
      try { const err = await response.json(); detail = err.detail || detail; } catch {}
      throw new Error(detail);
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Documentos_${data.nome_cedente.replace(/\s+/g,"_")}.zip`;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(a);

    showToast("✅ 4 documentos gerados com sucesso!", "success");
  } catch (err) {
    console.error(err);
    showToast(`❌ ${err.message}`, "error");
  } finally {
    btn.disabled = false;
    btn.innerHTML = "📦 Gerar TODOS os Documentos (.ZIP)";
  }
}
