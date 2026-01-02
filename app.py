import streamlit as st
import json
import os
import re
import random
import string
from datetime import datetime

# --- CONFIGURAÇÃO HUD STARK (TEMA MONDAY DARK) ---
st.set_page_config(page_title="J.A.R.V.I.S. | PROTOCOLO GABRIEL", layout="centered")

# CSS para manter o visual do seu CustomTkinter
st.markdown("""
    <style>
    .stApp { background-color: #1a1c1e; color: #e1e1e1; }
    [data-testid="stMetricValue"] { color: #00c875 !important; font-family: 'Segoe UI'; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #0085ff; }
    .monitor-text { 
        background-color: #111213; border: 1px solid #292c33; 
        padding: 10px; border-radius: 5px; font-family: 'Consolas'; color: #00c875;
    }
    .stButton>button {
        background-color: #292c33; color: white; border: 1px solid #0085ff;
        border-radius: 10px; height: 50px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARREGAR DADOS (missões.json) ---
def carregar_dados():
    if os.path.exists("missões.json"):
        with open("missões.json", 'r') as f: return json.load(f)
    return {"total": 0.0, "lista": []}

def salvar_dados(dados):
    with open("missões.json", 'w') as f:
        json.dump(dados, f, indent=4)

if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()

# --- INTERFACE ---
st.title("🛡️ JARVIS | PROTOCOLO FINAL")

# DASHBOARD
col1, col2 = st.columns(2)
with col1:
    st.metric("BALANÇO GERAL", f"R$ {st.session_state.dados['total']:.2f}")

with col2:
    limite = 2000.00
    progresso = min(st.session_state.dados['total'] / limite, 1.0)
    st.write(f"STATUS DO LIMITE")
    st.progress(progresso)

# MONITOR DE LOGS (Estilo o seu Monitor Textbox)
st.markdown("### 🖥️ MONITOR DE SISTEMA")
log_container = st.container()
with log_container:
    ts = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"<div class='monitor-text'>[{ts}] > SISTEMA ONLINE: AGUARDANDO COMANDO...</div>", unsafe_allow_html=True)

st.write("---")

# ENTRADA DE COMANDO (Substitui o seu Entry e Voz)
entrada = st.text_input("▶ DIGITE O GASTO OU COLE O PIX", placeholder="Ex: 50 reais lanche")

if entrada:
    # Lógica de extração de valor do seu código original
    valor_match = re.search(r'(\d+)', entrada)
    valor = float(valor_match.group(1)) if valor_match else 0.0
    
    # Se for um PIX (Payload)
    if "000201" in entrada:
        st.warning(f"PIX Detectado: R$ {valor:.2f}")
        if st.button("AUTORIZAR PAGAMENTO (MERCADO PAGO)"):
            st.session_state.dados["total"] += valor
            st.session_state.dados["lista"].insert(0, {
                "data": datetime.now().strftime("%Y-%m-%d"),
                "valor": valor, "desc": "Pagamento PIX", "metodo": "PIX", "categoria": "Financeiro"
            })
            salvar_dados(st.session_state.dados)
            # Abre o Mercado Pago no celular
            st.markdown(f'<a href="mercadopago://payments/main" target="_blank" style="color:white; background: #009ee3; padding: 15px; text-decoration: none; border-radius: 10px;">ABRIR MERCADO PAGO</a>', unsafe_allow_html=True)

    # Se for gasto manual
    elif valor > 0:
        if st.button(f"REGISTRAR GASTO: R$ {valor:.2f}"):
            st.session_state.dados["total"] += valor
            st.session_state.dados["lista"].insert(0, {
                "data": datetime.now().strftime("%Y-%m-%d"),
                "valor": valor, "desc": entrada, "metodo": "Manual", "categoria": "Geral"
            })
            salvar_dados(st.session_state.dados)
            st.success("Protocolo registrado, Gabriel.")
            st.rerun()

# HISTÓRICO MONDAY
st.write("---")
st.markdown("### 📑 HISTÓRICO MONDAY")
for item in st.session_state.dados["lista"][:10]:
    st.code(f" ▶ {item['data'][8:]}/{item['data'][5:7]} | R$ {item['valor']:8.2f} | {item['desc']}")