import streamlit as st
from helpers import recommends
import pandas as pd
from io import BytesIO


with st.sidebar:
    current_position = st.file_uploader(
        "(Optional) Enter a CSV file with your position in the format (ticker, stocks).",
    )

st.title("Sell Recommendations")

st.warning(
    """
    Take the following list at most as a starting point for you own analysis.
    
    Every investment decision should be thoughtful and you are the sole responsible for them.  
    """,
    icon="⚠️",
)

gov_bond_rate = st.slider(
    "Enter the long-term government bond rate: ",
    min_value=0.02,
    max_value=0.15,
    value=0.10,
    key="GovRate",
)

sell_recommends = recommends(kind="sell", gov_bond_rate=gov_bond_rate)

if current_position:
    position = pd.read_csv(
        BytesIO(current_position.read()), header=None, names=["ticker", "position"]
    )
    sell_recommends = sell_recommends.merge(position, how="left", on="ticker").fillna(
        {"position": 0}
    )

st.write(f"Found {sell_recommends.shape[0]} sell recommendations:")
st.dataframe(sell_recommends, hide_index=True, height=250)
