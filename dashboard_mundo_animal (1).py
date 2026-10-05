import streamlit as st
import pandas as pd
import unicodedata
import re

st.set_page_config(
    page_title="Mundo Animal | Painel",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SHEET_ID = "1RJ22PgAdtbN8Kx96XUrFd3pKAjvdMFmi"
SHEET_NAME = "Planilha1"
CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq"
    f"?tqx=out:csv&sheet={SHEET_NAME}"
)

st.markdown("""
<style>
.block-container {padding-top: 1rem; padding-bottom: 2rem;}
.main-title {font-size: 2rem; font-weight: 800; margin-bottom: .15rem;}
.sub {color:#666; margin-bottom:1rem;}
[data-testid="stMetricValue"] {font-size: 2rem;}
@media (max-width: 700px) {
  .block-container {padding-left: .8rem; padding-right: .8rem;}
  .main-title {font-size: 1.45rem;}
  [data-testid="stMetricValue"] {font-size: 1.35rem;}
}
</style>
""", unsafe_allow_html=True)

def chave(txt):
    txt = "" if txt is None else str(txt)
    txt = txt.replace("\xa0", " ").strip()
    txt = " ".join(txt.split())
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return txt.upper()

@st.cache_data(ttl=30)
def carregar():
    df = pd.read_csv(CSV_URL)

    # Limpa cabeçalhos e remove colunas vazias/sem nome
    df.columns = [str(c).replace("\xa0", " ").strip() for c in df.columns]
    df = df.loc[:, ~df.columns.str.match(r"^Sem nome:|^Unnamed:", case=False)]

    # Mapa flexível de nomes reais -> nomes usados pelo painel
    aliases = {
        "COLUNA 1": "CÓDIGO TRAY",
        "CODIGO TRAY": "CÓDIGO TRAY",
        "CÓDIGO TRAY": "CÓDIGO TRAY",
        "NOME DO PRODUTO": "NOME DO PRODUTO",
        "CONFERIDO": "CONFERIDO",
        "OBSERVACAO CONFERENCIA": "OBSERVAÇÃO CONFERÊNCIA",
        "OBSERVAÇÃO CONFERÊNCIA": "OBSERVAÇÃO CONFERÊNCIA",
        "MERCADO LIVRE": "MERCADO LIVRE",
        "CONTADO ESTOQUE": "CONTADO ESTOQUE",
        "AMAURI PRECO": "AMAURI PREÇO",
        "AMAURI PREÇO": "AMAURI PREÇO",
        "OBSERVACAO AMAURI": "OBSERVAÇÃO AMAURI",
        "OBSERVAÇÃO AMAURI": "OBSERVAÇÃO AMAURI",
        "STATUS GERAL": "STATUS GERAL",
    }

    renomear = {}
    for col in df.columns:
        k = chave(col)
        if k in aliases:
            renomear[col] = aliases[k]

    df = df.rename(columns=renomear)

    # Só considera linhas que realmente têm produto
    if "NOME DO PRODUTO" in df.columns:
        df = df[df["NOME DO PRODUTO"].notna()]
        df = df[df["NOME DO PRODUTO"].astype(str).str.strip() != ""]

    return df.reset_index(drop=True)

def norm(v):
    if pd.isna(v):
        return ""
    return chave(v)

try:
    df = carregar()
except Exception as e:
    st.error("Não consegui ler a planilha online.")
    st.code(str(e))
    st.stop()

COL_COD = "CÓDIGO TRAY"
COL_NOME = "NOME DO PRODUTO"
COL_CONF = "CONFERIDO"
COL_OBS_CONF = "OBSERVAÇÃO CONFERÊNCIA"
COL_ML = "MERCADO LIVRE"
COL_ESTOQUE = "CONTADO ESTOQUE"
COL_PRECO = "AMAURI PREÇO"
COL_OBS_AMAURI = "OBSERVAÇÃO AMAURI"
COL_STATUS = "STATUS GERAL"

necessarias = [COL_NOME, COL_CONF, COL_ML, COL_ESTOQUE, COL_PRECO, COL_STATUS]
faltando = [c for c in necessarias if c not in df.columns]

if faltando:
    st.error("Ainda faltam colunas necessárias para montar o painel.")
    st.write("Faltando:", faltando)
    st.write("Encontradas:", list(df.columns))
    st.stop()

total = len(df)
conferidos = (df[COL_CONF].map(norm) == "SIM").sum()
ml_ok = (df[COL_ML].map(norm) == "SIM").sum()
estoque_ok = (df[COL_ESTOQUE].map(norm) == "SIM").sum()
preco_ok = (df[COL_PRECO].map(norm) == "SIM").sum()
completos = (df[COL_STATUS].map(norm) == "100% PUBLICADO").sum()
pendentes = total - completos

st.markdown('<div class="main-title">🐾 Mundo Animal — Painel de Publicação</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub">Planilha compartilhada • dados atualizados automaticamente</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)
c1.metric("📦 Total", total)
c2.metric("✅ 100% publicados", completos)
c3.metric("⏳ Pendentes", pendentes)

percentual = (completos / total * 100) if total else 0
st.progress(completos / total if total else 0, text=f"Progresso geral: {percentual:.1f}%")

st.divider()
st.subheader("Andamento por etapa")

m1, m2 = st.columns(2)
with m1:
    st.metric("Conferência", f"{conferidos}/{total}", f"{conferidos/total*100:.1f}%" if total else "0%")
    st.metric("Mercado Livre", f"{ml_ok}/{total}", f"{ml_ok/total*100:.1f}%" if total else "0%")
with m2:
    st.metric("Estoque contado", f"{estoque_ok}/{total}", f"{estoque_ok/total*100:.1f}%" if total else "0%")
    st.metric("Preço Amauri", f"{preco_ok}/{total}", f"{preco_ok/total*100:.1f}%" if total else "0%")

graf = pd.DataFrame({
    "Etapa": ["Conferência", "Mercado Livre", "Estoque contado", "Preço Amauri"],
    "Concluídos": [conferidos, ml_ok, estoque_ok, preco_ok],
}).set_index("Etapa")

st.bar_chart(graf, horizontal=True)

st.divider()
st.subheader("O que precisa de atenção")

opcao = st.selectbox(
    "Filtro",
    [
        "Todos os pendentes",
        "Não conferidos",
        "Mercado Livre pendente",
        "Estoque pendente",
        "Preço pendente",
    ],
)

if opcao == "Todos os pendentes":
    mask = df[COL_STATUS].map(norm) != "100% PUBLICADO"
elif opcao == "Não conferidos":
    mask = df[COL_CONF].map(norm) != "SIM"
elif opcao == "Mercado Livre pendente":
    mask = df[COL_ML].map(norm) != "SIM"
elif opcao == "Estoque pendente":
    mask = df[COL_ESTOQUE].map(norm) != "SIM"
else:
    mask = df[COL_PRECO].map(norm) != "SIM"

cols = []
for c in [COL_COD, COL_NOME, COL_CONF, COL_ML, COL_ESTOQUE, COL_PRECO, COL_STATUS, COL_OBS_CONF, COL_OBS_AMAURI]:
    if c in df.columns:
        cols.append(c)

pend = df.loc[mask, cols].copy()
st.caption(f"{len(pend)} produto(s) neste filtro")
st.dataframe(pend, use_container_width=True, hide_index=True, height=520)

if st.button("🔄 Atualizar agora"):
    st.cache_data.clear()
    st.rerun()

st.caption("Fonte: Google Sheets compartilhado da Mundo Animal")
