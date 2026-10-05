st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background: #ffffff !important;
    color: #111111 !important;
}

[data-testid="stHeader"] {
    background: #ffffff !important;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

.main-title {
    font-size: 2.7rem;
    font-weight: 900;
    line-height: 1.2;
    margin-top: 0.6rem;
    margin-bottom: 0.4rem;
    color: #111111;
}

.sub {
    color: #4b5563;
    font-size: 1.25rem;
    font-weight: 500;
    margin-bottom: 1.8rem;
}

h1, h2, h3 {
    color: #111111 !important;
}

h2 {
    font-size: 2.1rem !important;
    font-weight: 900 !important;
}

h3 {
    font-size: 1.8rem !important;
    font-weight: 850 !important;
}


/* CARDS */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 2px solid #e5e7eb;
    padding: 24px 26px;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    min-height: 150px;
}


/* TÍTULO DO CARD */
[data-testid="stMetricLabel"] {
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    color: #111111 !important;
}


/* NÚMERO GRANDE */
[data-testid="stMetricValue"] {
    font-size: 2.7rem !important;
    font-weight: 900 !important;
    color: #000000 !important;
}


/* PORCENTAGEM */
[data-testid="stMetricDelta"] {
    font-size: 1.2rem !important;
    font-weight: 800 !important;
}


/* TEXTO VERDE MAIS ESCURO */
[data-testid="stMetricDelta"] svg,
[data-testid="stMetricDelta"] > div {
    color: #08783d !important;
    fill: #08783d !important;
}


/* FUNDO DO DELTA VERDE */
[data-testid="stMetricDelta"] {
    background-color: #d9fbe8 !important;
    padding: 5px 11px !important;
    border-radius: 999px !important;
    width: fit-content;
}


/* PROGRESSO */
[data-testid="stProgress"] {
    margin-top: 10px;
    margin-bottom: 20px;
}

[data-testid="stProgress"] p {
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    color: #111111 !important;
}


/* SELECT */
.stSelectbox label {
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    color: #111111 !important;
}


/* TABELA */
[data-testid="stDataFrame"] {
    border: 1px solid #d1d5db;
    border-radius: 14px;
    overflow: hidden;
}


/* TEXTOS GERAIS */
div[data-testid="stMarkdownContainer"] p {
    font-size: 1.12rem;
    color: #111111;
}


/* DIVISÓRIA */
hr {
    border-color: #d1d5db !important;
}


/* CELULAR */
@media (max-width: 700px) {

    .block-container {
        padding-top: 2.4rem;
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .main-title {
        font-size: 2rem;
    }

    .sub {
        font-size: 1.05rem;
    }

    h2 {
        font-size: 1.7rem !important;
    }

    h3 {
        font-size: 1.45rem !important;
    }

    [data-testid="stMetric"] {
        padding: 18px 16px;
        min-height: 125px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 1.08rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
}

</style>
""", unsafe_allow_html=True)
