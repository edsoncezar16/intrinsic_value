import streamlit as st
import numpy as np
from helpers import load_portfolio_data

st.set_page_config(page_title="Portfolio Builder", layout="wide")

# Language selector
lang = st.selectbox("Language / Idioma", ["English", "Português (BR)"], index=0)

# Load portfolio data
df = load_portfolio_data()

# Labels for translations
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

# Current language context
L = labels[lang]

if df.empty:
    st.warning(L["no_data"])
    st.stop()

# Compute weights
df["weight"] = 2 * df["margin_of_safety"] - 1
df["normalized_weight"] = df["weight"] / df["weight"].sum()

# Capital input
capital = st.number_input(
    label=L["capital_label"], min_value=0.0, value=10000.0, step=100.0, format="%.2f"
)

# Allocation mode toggle
allocation_mode = st.radio(
    label=L["toggle_label"],
    options=L["toggle_options"],
    index=0,
    horizontal=True,
)

# Allocation logic
df["allocated_capital"] = df["normalized_weight"] * capital

if allocation_mode == L["toggle_options"][0]:  # Lot mode
    df["lots"] = np.floor(df["allocated_capital"] / (df["market_price"] * 100))
    df["shares"] = df["lots"] * 100
    st.info(L["info_lot"])
else:  # Unit mode
    df["shares"] = np.floor(df["allocated_capital"] / df["market_price"])
    st.info(L["info_unit"])

df["total_cost"] = df["shares"] * df["market_price"]
df["remaining_cash"] = capital - df["total_cost"].sum()

# Display results
st.title(L["title"])
st.subheader(L["section_header"])

display_df = df[
    [
        "ticker",
        "company_name",
        "market_price",
        "margin_of_safety",
        "normalized_weight",
        "shares",
        "total_cost",
    ]
].rename(columns=L["columns"])

st.dataframe(display_df, use_container_width=True, hide_index=True)

# Capital summary
st.markdown(L["capital_used"].format(df["total_cost"].sum()))
st.markdown(L["cash_remaining"].format(df["remaining_cash"].iloc[0]))
