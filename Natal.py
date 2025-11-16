import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image
import base64

SENHA_ADMIN = "Vitoria123@"

# Configuração da página
st.set_page_config(
    page_title="🎅 Natal em Família — RSVP",
    page_icon="🎄",
    layout="centered"
)

# ❄️ NEVE (funciona em PC e celular)
st.markdown("""
<style>

.snowflake {
    position: fixed;
    top: -10px;
    color: white;
    font-size: 1em;
    animation-name: fall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
    z-index: 9999;
    pointer-events: none;
}

@keyframes fall {
    0% { top: -10px; opacity: 1; }
    100% { top: 110vh; opacity: 0; }
}

</style>

<div id="snow-container"></div>

<script>
const snowContainer = document.getElementById('snow-container');
for (let i = 0; i < 45; i++) {
    let snow = document.createElement('div');
    snow.className = 'snowflake';
    snow.innerHTML = '❄';
    snow.style.left = Math.random() * 100 + 'vw';
    snow.style.fontSize = (12 + Math.random() * 18) + 'px';
    snow.style.animationDuration = (6 + Math.random() * 6) + 's';
    snow.style.animationDelay = Math.random() * 5 + 's';
    snow.style.opacity = (0.3 + Math.random() * 0.7);
    snowContainer.appendChild(snow);
}
</script>
""", unsafe_allow_html=True)

# 🎄 Estilos natalinos + correção de cor no celular
st.markdown("""
<style>

.stApp {
    background: #fff5f5 !important;
    background-image: radial-gradient(circle at top, #ffe5e5, #fff5f5 70%) !important;
    background-attachment: fixed !important;
}

/* Corrige fundo no celular */
@media (max-width: 600px) {
    .stApp {
        background: #fff5f5 !important;
        background-image: radial-gradient(circle at top, #ffe5e5, #fff5f5 85%) !important;
        background-size: cover !important;
    }
}

.title {
    font-weight: 800;
    font-size: 38px;
    text-align: center;
    color: #b30000;
    text-shadow: 1px 1px 2px #ffcccc;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

.card {
    background: rgba(255,255,255,0.90);
    padding: 20px;
    border-radius: 14px; 
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
}

.metric-card {
    background: rgba(255,255,255,0.8);
    padding: 16px;
    border-radius: 12px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<div class='title'>🎄 Natal em Família 🎅</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Confirme sua presença e ajude a organizar nossa ceia! 🌟</div>", unsafe_allow_html=True)

DATA_FILE = "rsvp_responses.csv"

# Criar arquivo se não existir
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "timestamp", "nome", "confirmacao", "adultos", "criancas", 
        "prato", "restricoes", "mensagem"
    ])
    df_init.to_csv(DATA_FILE, index=False)

# Formulário
st.markdown("<div class='card'>", unsafe_allow_html=True)

with st.form("rsvp_form"):
    nome = st.text_input("🎁 Seu nome completo")

    confirmacao = st.radio("🎅 Você confirma presença?", ("Sim", "Não", "Talvez"))

    col1, col2 = st.columns(2)
    with col1:
        adultos = st.number_input("👨‍👩‍👧‍👦 Adultos", 0, 20, 1)
    with col2:
        criancas = st.number_input("🧒 Crianças", 0, 10, 0)

    prato = st.text_input("🍽 Qual prato vai levar?")
    restricoes = st.multiselect(
        "⚠️ Restrições / Preferências alimentares",
        ["Sem glúten", "Sem lactose", "Vegetariano", "Vegano", "Sem castanhas", "Nenhuma"],
        default=["Nenhuma"]
    )
    mensagem = st.text_area("💌 Deixe uma mensagem especial (opcional)", max_chars=300)

    submitted = st.form_submit_button("🎄 Confirmar presença 🎅")

    st.markdown("</div>", unsafe_allow_html=True)

# Salvando no CSV
if submitted:
    if not nome:
        st.warning("Por favor, insira seu nome para continuar.")
    else:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        novo = {
            "timestamp": ts,
            "nome": nome,
            "confirmacao": confirmacao,
            "adultos": adultos,
            "criancas": criancas,
            "prato": prato,
            "restricoes": ", ".join(restricoes),
            "mensagem": mensagem
        }

        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success("🎅 Ho ho ho! Sua presença foi registrada com sucesso! 🎄✨")

# Área administrativa
st.markdown("---")
st.subheader("🔒 Área Administrativa")

senha = st.text_input("Digite a senha para continuar", type="password")

try:
    df = pd.read_csv(DATA_FILE)
except:
    df = pd.DataFrame()

if senha == SENHA_ADMIN:

    st.success("Acesso liberado! 🎅")

    if not df.empty:
        total_confirmados = (
            df[df["confirmacao"] == "Sim"]["adultos"].sum() +
            df[df["confirmacao"] == "Sim"]["criancas"].sum()
        )
        count_sim = df[df["confirmacao"] == "Sim"].shape[0]
        count_nao = df[df["confirmacao"] == "Não"].shape[0]
        count_talvez = df[df["confirmacao"] == "Talvez"].shape[0]

        colA, colB, colC, colD = st.columns(4)

        colA.metric("🎁 Pessoas", int(total_confirmados))
        colB.metric("🎄 Confirmados", int(count_sim))
        colC.metric("🙅‍♂️ Não vêm", int(count_nao))
        colD.metric("🤔 Talvez", int(count_talvez))

        st.markdown("### 📋 Lista completa")
        st.dataframe(df.sort_values(by="timestamp", ascending=False))

        # Download CSV
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="rsvp_responses.csv">⬇️ Baixar respostas (CSV)</a>'
        st.markdown(href, unsafe_allow_html=True)

else:
    st.info("Área restrita. Digite a senha para ver os convidados.")

st.markdown("---")
st.caption("🎄 Feito com carinho para reunir a família — Feliz Natal! ✨")

# python -m streamlit run Natal.py
