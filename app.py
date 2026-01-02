import streamlit as st
import json
import os
import re
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="J.A.R.V.I.S. | PROTOCOLO STARK", layout="centered")

# Função para o Jarvis falar no celular
def jarvis_falar_js(texto):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{texto}');
    msg.lang = 'pt-BR';
    msg.rate = 1.2;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# Carregar Banco de Dados
if os.path.exists("missões.json"):
    with open("missões.json", 'r') as f:
        dados = json.load(f)
else:
    dados = {"total": 0.0, "lista": []}

st.title("🛡️ JARVIS: SISTEMA DE DEFESA")

# --- ESCANEAR QR CODE ---
st.write("### 📸 ESCANEAR CÓDIGO PIX")
# Esse comando abre a câmera do seu celular direto no site
img_file = st.camera_input("APONTE PARA O QR CODE")

if img_file:
    # Simulação de OCR (Como o EasyOCR é pesado para o servidor, 
    # ele registra que a imagem foi capturada para processamento)
    jarvis_falar_js("Imagem capturada. Analisando padrões de criptografia, Gabriel.")
    st.warning("⚠️ Processando visão computacional...")

# --- REGISTRO POR VOZ / TEXTO ---
st.write("---")
entrada = st.text_input("▶ COMANDO DE VOZ (DIGITE O QUE COMPROU)")

if st.button("EXECUTAR PROTOCOLO"):
    valor_m = re.search(r'(\d+)', entrada)
    valor = float(valor_m.group(1)) if valor_m else 0.0
    
    if valor > 0:
        dados["total"] += valor
        dados["lista"].insert(0, {"data": datetime.now().strftime("%Y-%m-%d"), "valor": valor, "desc": entrada})
        
        with open("missões.json", 'w') as f:
            json.dump(dados, f, indent=4)
            
        # O JARVIS FALA AQUI:
        jarvis_falar_js(f"Protocolo registrado com sucesso. Gastos totais em {dados['total']} reais. Bom trabalho, Gabriel.")
        st.success(f"R$ {valor} computado.")
        st.rerun()

st.metric("BALANÇO ATUAL", f"R$ {dados['total']:.2f}")