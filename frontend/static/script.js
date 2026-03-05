const API_URL = "";

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
  if (!padrao || !branded) return;
  const val = document.querySelector('input[name="template_type"]:checked')?.value;
  padrao.classList.toggle("selected", val === "padrao");
  branded.classList.toggle("selected", val === "branded");
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
  // Clear previous invalid states
  document.querySelectorAll(".invalid").forEach(el => el.classList.remove("invalid"));
  required.forEach(name => {
    const el = document.getElementById(name);
    if (el && !el.value.trim()) {
      el.classList.add("invalid");
      valid = false;
    }
  });
  return valid;
}

document.addEventListener("DOMContentLoaded", () => {
  resetLawyers();
  setDefaultDates();

  // Mask CPF fields
  ["cpf_cedente","cpf_cessionario","outorgado_cpf_2"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", () => maskCPF(el));
  });

  // Mask CEP fields
  ["cep_cedente","cep_cessionario"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", () => maskCEP(el));
  });

  // Auto-calc liquido
  const vb = document.getElementById("valor_bruto");
  const pct = document.getElementById("percentual_honorarios");
  if (vb) vb.addEventListener("input", calcLiquido);
  if (pct) pct.addEventListener("input", calcLiquido);

  // Form submit
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
    showToast("❌ Preencha todos os campos obrigatórios!", "error");
    // Scroll to first invalid
    const first = document.querySelector(".invalid");
    if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }

  // Format dates
  data.data_nascimento = formatDate(data.data_nascimento);
  data.data_contrato = formatDate(data.data_contrato);
  data.data_negociacao = formatDate(data.data_negociacao);

  // Numerics
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
