import streamlit as st
import pandas as pd
import unicodedata

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

html, body, [data-testid="stAppViewContainer"] {
    background: #ffffff !important;
    color: #111827 !important;
}

[data-testid="stHeader"] {
    background: #ffffff !important;
}

.block-container {
    padding-top: 3.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1.2;
    margin-top: 0.6rem;
    margin-bottom: 0.35rem;
    color: #111827;
}

.sub {
    color: #6b7280;
    font-size: 1.15rem;
    margin-bottom: 1.8rem;
}

h1, h2, h3 {
    color: #111827 !important;
}

h2 {
    font-size: 2rem !important;
    font-weight: 800 !important;
}

h3 {
    font-size: 1.65rem !important;
    font-weight: 750 !important;
}

[data-testid="stMetric"] {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    padding: 18px 20px;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

[data-testid="stMetricLabel"] {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #374151 !important;
}

[data-testid="stMetricValue"] {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    color: #111827 !important;
}

[data-testid="stMetricDelta"] {
    font-size: 1rem !important;
}

[data-testid="stProgressBar"] > div > div {
    height: 16px !important;
    border-radius: 999px !important;
}

.stSelectbox label {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #111827 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    overflow: hidden;
}

div[data-testid="stMarkdownContainer"] p {
    font-size: 1.05rem;
}

hr {
    border-color: #e5e7eb !important;
}

@media (max-width: 700px) {

    .block-container {
        padding-top: 2.5rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .main-title {
        font-size: 1.8rem;
    }

    .sub {
        font-size: 1rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
    }

    h2 {
        font-size: 1.55rem !important;
    }

    h3 {
        font-size: 1.3rem !important;
    }
}

</style>
""", unsafe_allow_html=True)


def chave(txt):
    txt = "" if txt is None else str(txt)
    txt = txt.replace("\xa0", " ").strip()
    txt = " ".join(txt.split())
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(
        c for c in txt
        if not unicodedata.combining(c)
    )
    return txt.upper()


@st.cache_data(ttl=30)
def carregar():
    df = pd.read_csv(CSV_URL)

    df.columns = [
        str(c).replace("\xa0", " ").strip()
        for c in df.columns
    ]

    df = df.loc[
        :,
        ~df.columns.str.match(
            r"^Sem nome:|^Unnamed:",
            case=False
        )
    ]

    aliases = {
        "COLUNA 1": "CÓDIGO TRAY",
        "CODIGO TRAY": "CÓDIGO TRAY",
        "NOME DO PRODUTO": "NOME DO PRODUTO",
        "CONFERIDO": "CONFERIDO",
        "OBSERVACAO CONFERENCIA": "OBSERVAÇÃO CONFERÊNCIA",
        "MERCADO LIVRE": "MERCADO LIVRE",
        "CONTADO ESTOQUE": "CONTADO ESTOQUE",
        "AMAURI PRECO": "AMAURI PREÇO",
        "OBSERVACAO AMAURI": "OBSERVAÇÃO AMAURI",
        "STATUS GERAL": "STATUS GERAL",
    }

    renomear = {}

    for col in df.columns:
        k = chave(col)
        if k in aliases:
            renomear[col] = aliases[k]

    df = df.rename(columns=renomear)

    if "NOME DO PRODUTO" in df.columns:
        df = df[df["NOME DO PRODUTO"].notna()]
        df = df[
            df["NOME DO PRODUTO"]
            .astype(str)
            .str.strip()
            != ""
        ]

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


necessarias = [
    COL_NOME,
    COL_CONF,
    COL_ML,
    COL_ESTOQUE,
    COL_PRECO,
    COL_STATUS
]

faltando = [
    c for c in necessarias
    if c not in df.columns
]

if faltando:
    st.error(
        "Ainda faltam colunas necessárias "
        "para montar o painel."
    )
    st.write("Faltando:", faltando)
    st.write("Encontradas:", list(df.columns))
    st.stop()


total = len(df)

conferidos = (
    df[COL_CONF].map(norm) == "SIM"
).sum()

ml_ok = (
    df[COL_ML].map(norm) == "SIM"
).sum()

estoque_ok = (
    df[COL_ESTOQUE].map(norm) == "SIM"
).sum()

preco_ok = (
    df[COL_PRECO].map(norm) == "SIM"
).sum()

completos = ml_ok
pendentes = total - completos


st.markdown(
    '<div class="main-title">'
    '🐾 Mundo Animal — Painel de Publicação'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub">'
    'Acompanhamento em tempo real da planilha compartilhada'
    '</div>',
    unsafe_allow_html=True
)


c1, c2, c3 = st.columns(3)

c1.metric(
    "📦 Total de produtos",
    total
)

c2.metric(
    "✅ Publicados no Mercado Livre",
    completos
)

c3.metric(
    "⏳ Pendentes no Mercado Livre",
    pendentes
)


percentual = (
    completos / total * 100
    if total
    else 0
)

st.progress(
    completos / total if total else 0,
    text=f"Progresso geral: {percentual:.1f}%"
)


st.divider()

st.subheader("📊 Andamento por etapa")


m1, m2 = st.columns(2)

with m1:
    st.metric(
        "✅ Conferência",
        f"{conferidos}/{total}",
        f"{conferidos/total*100:.1f}%"
        if total
        else "0%"
    )

    st.metric(
        "🛒 Mercado Livre",
        f"{ml_ok}/{total}",
        f"{ml_ok/total*100:.1f}%"
        if total
        else "0%"
    )


with m2:
    st.metric(
        "📦 Estoque contado",
        f"{estoque_ok}/{total}",
        f"{estoque_ok/total*100:.1f}%"
        if total
        else "0%"
    )

    st.metric(
        "💰 Preço Amauri",
        f"{preco_ok}/{total}",
        f"{preco_ok/total*100:.1f}%"
        if total
        else "0%"
    )


graf = pd.DataFrame({
    "Etapa": [
        "Conferência",
        "Mercado Livre",
        "Estoque contado",
        "Preço Amauri"
    ],
    "Concluídos": [
        conferidos,
        ml_ok,
        estoque_ok,
        preco_ok
    ],
}).set_index("Etapa")


st.bar_chart(
    graf,
    horizontal=True
)


st.divider()

st.subheader("⚠️ O que precisa de atenção")


opcao = st.selectbox(
    "Escolha o filtro",
    [
        "Todos os pendentes",
        "Não conferidos",
        "Mercado Livre pendente",
        "Estoque pendente",
        "Preço pendente",
    ],
)


if opcao == "Todos os pendentes":
    mask = (
        df[COL_ML].map(norm)
        != "SIM"
    )

elif opcao == "Não conferidos":
    mask = (
        df[COL_CONF].map(norm)
        != "SIM"
    )

elif opcao == "Mercado Livre pendente":
    mask = (
        df[COL_ML].map(norm)
        != "SIM"
    )

elif opcao == "Estoque pendente":
    mask = (
        df[COL_ESTOQUE].map(norm)
        != "SIM"
    )

else:
    mask = (
        df[COL_PRECO].map(norm)
        != "SIM"
    )


cols = []

for c in [
    COL_COD,
    COL_NOME,
    COL_CONF,
    COL_ML,
    COL_ESTOQUE,
    COL_PRECO,
    COL_STATUS,
    COL_OBS_CONF,
    COL_OBS_AMAURI
]:
    if c in df.columns:
        cols.append(c)


pend = df.loc[
    mask,
    cols
].copy()


st.caption(
    f"{len(pend)} produto(s) encontrado(s)"
)

st.dataframe(
    pend,
    use_container_width=True,
    hide_index=True,
    height=520
)


if st.button("🔄 Atualizar agora"):
    st.cache_data.clear()
    st.rerun()


st.caption(
    "Fonte: Google Sheets compartilhado da Mundo Animal"
)
   

         
