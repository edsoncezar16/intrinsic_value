import streamlit as st
import numpy as np
from helpers import load_portfolio_data

st.title("Margin of Safety Portfolio Builder")

st.markdown("""
This tool builds a stock portfolio using only companies with a **margin of safety greater than 50%**,
assigning weights using the formula:

$$
\\text{Weight} = 2 \\times \\text{MoS} - 1
$$

Enter your total capital to calculate the number of shares to purchase for each selected stock.
""")


df = load_portfolio_data()

if df.empty:
    st.warning("No stocks found with margin of safety greater than 50%.")
    st.stop()

# --- Compute weights
df["weight"] = 2 * df["margin_of_safety"] - 1
df["normalized_weight"] = df["weight"] / df["weight"].sum()

# --- User input
capital = st.number_input(
    "Enter your total investment capital (R$):",
    min_value=0.0,
    value=10000.0,
    step=100.0,
)

# --- Allocation and shares
df["allocated_capital"] = df["normalized_weight"] * capital
df["shares"] = np.floor(df["allocated_capital"] / df["market_price"])
df["total_cost"] = df["shares"] * df["market_price"]

# --- Display
st.subheader("Suggested Portfolio")

st.dataframe(
    df[
        [
            "ticker",
            "company_name",
            "market_price",
            "margin_of_safety",
            "normalized_weight",
            "shares",
            "total_cost",
        ]
    ],
    use_container_width=True,
)

st.markdown(f"**Total capital used:** R$ {df['total_cost'].sum():,.2f}")
st.markdown(f"**Remaining cash:** R$ {capital - df['total_cost'].sum():,.2f}")
