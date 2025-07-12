import streamlit as st
import numpy as np
from helpers import load_portfolio_data

st.set_page_config(page_title="Construtor de Portfólio", layout="wide")

# Initialize session state language if not set
if "lang" not in st.session_state:
    st.session_state.lang = "Português (BR)"

# Language selector with persistence
lang = st.selectbox(
    "Idioma / Language",
    ["Português (BR)", "English"],
    index=["Português (BR)", "English"].index(st.session_state.lang),
)
st.session_state.lang = lang

# Load data
df = load_portfolio_data()

# Labels per language
labels = {
    "English": {
        "title": "Portfolio Builder",
        "capital_label": "Enter your total investment capital (R$):",
        "no_data": "No stocks found with margin of safety greater than 50%.",
        "toggle_label": "Allocation mode:",
        "toggle_options": ["Standard B3 lots (100 shares)", "Individual shares"],
        "info_lot": "Note: Share quantities are rounded down to the nearest lot of 100 shares, as per standard B3 trading rules.",
        "info_unit": "Note: Share quantities are rounded down to the nearest individual share.",
        "section_header": "Suggested Portfolio",
        "columns": {
            "ticker": "Ticker",
            "company_name": "Company",
            "market_price": "Market Price (R$)",
            "margin_of_safety": "Margin of Safety",
            "normalized_weight": "Portfolio Weight",
            "shares": "Shares to Buy",
            "total_cost": "Total Cost (R$)",
        },
        "capital_used": "**Total capital used:** R$ {:.2f}",
        "cash_remaining": "**Remaining cash:** R$ {:.2f}",
    },
    "Português (BR)": {
        "title": "Construtor de Portfólio",
        "capital_label": "Informe o capital total para investir (R$):",
        "no_data": "Nenhuma ação encontrada com margem de segurança superior a 50%.",
        "toggle_label": "Modo de alocação:",
        "toggle_options": ["Lotes padrão da B3 (100 ações)", "Ações individuais"],
        "info_lot": "Nota: A quantidade de ações é arredondada para baixo ao lote de 100 ações, conforme padrão da B3.",
        "info_unit": "Nota: A quantidade de ações é arredondada para baixo à unidade.",
        "section_header": "Portfólio Sugerido",
        "columns": {
            "ticker": "Ticker",
            "company_name": "Empresa",
            "market_price": "Preço de Mercado (R$)",
            "margin_of_safety": "Margem de Segurança",
            "normalized_weight": "Peso no Portfólio",
            "shares": "Ações a Comprar",
            "total_cost": "Custo Total (R$)",
        },
        "capital_used": "**Capital utilizado:** R$ {:.2f}",
        "cash_remaining": "**Saldo restante:** R$ {:.2f}",
    },
}

L = labels[lang]

# Handle no data case
if df.empty:
    st.warning(L["no_data"])
    st.stop()

# Compute weights
df["weight"] = 2 * df["margin_of_safety"] - 1
df["normalized_weight"] = df["weight"] / df["weight"].sum()

# User input: total capital
capital = st.number_input(
    label=L["capital_label"], min_value=0.0, value=10000.0, step=100.0, format="%.2f"
)

# User input: allocation mode
allocation_mode = st.radio(
    label=L["toggle_label"],
    options=L["toggle_options"],
    index=0,
    horizontal=True,
)

# Compute allocation
df["allocated_capital"] = df["normalized_weight"] * capital

if allocation_mode == L["toggle_options"][0]:  # Lote de 100 ações
    df["lots"] = np.floor(df["allocated_capital"] / (df["market_price"] * 100))
    df["shares"] = df["lots"] * 100
    st.info(L["info_lot"])
else:  # Ações individuais
    df["shares"] = np.floor(df["allocated_capital"] / df["market_price"])
    st.info(L["info_unit"])

df["total_cost"] = df["shares"] * df["market_price"]
df["remaining_cash"] = capital - df["total_cost"].sum()

# Display table
st.title(L["title"])
st.subheader(L["section_header"])

columns = [
    "ticker",
    "company_name",
    "market_price",
    "margin_of_safety",
    "normalized_weight",
    "shares",
    "total_cost",
]

display_df = df[columns].rename(columns=L["columns"])
st.dataframe(display_df, use_container_width=True, hide_index=True)

# Summary
st.markdown(L["capital_used"].format(df["total_cost"].sum()))
st.markdown(L["cash_remaining"].format(df["remaining_cash"].iloc[0]))
