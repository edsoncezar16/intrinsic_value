import streamlit as st
import numpy as np
from helpers import state, lang, load

st.set_page_config(page_title="Construtor de Portfólio", layout="wide")

# ----- Setup -----
state.init_session_state()
lang_code = state.language_selector()
L = lang.get_labels()[lang_code]
allocation_mode = state.allocation_mode_selector(L["toggle_label"])

# ----- Load Data -----
df = load.portfolio_data()
if df.empty:
    st.warning(L["no_data"])
    st.stop()

# ----- Capital Input -----
st.title(L["title"])
capital = st.number_input(
    label=L["capital_label"], min_value=0.0, value=10000.0, step=100.0, format="%.2f"
)

# ----- Weight Computation -----
df["weight"] = 2 * df["margin_of_safety"] - 1
df["normalized_weight"] = df["weight"] / df["weight"].sum()
df["allocated_capital"] = df["normalized_weight"] * capital

# ----- Share Allocation -----
if allocation_mode == L["toggle_options"][0]:  # Lot mode
    df["lots"] = np.floor(df["allocated_capital"] / (df["market_price"] * 100))
    df["shares"] = df["lots"] * 100
    st.info(L["info_lot"])
else:  # Unit mode
    df["shares"] = np.floor(df["allocated_capital"] / df["market_price"])
    st.info(L["info_unit"])

df["total_cost"] = df["shares"] * df["market_price"]
df["remaining_cash"] = capital - df["total_cost"].sum()

# ----- Display Table -----
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

# ----- Summary -----
st.markdown(L["capital_used"].format(df["total_cost"].sum()))
st.markdown(L["cash_remaining"].format(df["remaining_cash"].iloc[0]))
