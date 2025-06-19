import streamlit as st
from helpers import recommends
import pandas as pd
from io import BytesIO

pd.options.plotting.backend = "plotly"

with st.sidebar:
    current_position = st.file_uploader(
        "(Optional) Enter a CSV file with your position in the format (ticker, stocks).",
    )

st.title("Buy Recommendations")

st.warning(
    """
    Take the following list at most as a starting point for you own analysis.
    
    Every investment decision should be thoughtful and you are the sole responsible for them.  
    """,
    icon="⚠️",
)

margin_of_safety = st.slider(
    "Enter you minimum acceptable margin of safety: ",
    min_value=0.1,
    max_value=0.5,
    value=0.5,
    key="MoS",
)

gov_bond_rate = st.slider(
    "Enter the long-term government bond rate: ",
    min_value=0.02,
    max_value=0.15,
    value=0.10,
    key="GovRate",
)

buy_recommends = recommends(
    kind="buy", margin_of_safety=margin_of_safety, gov_bond_rate=gov_bond_rate
)


if current_position:
    position = pd.read_csv(
        BytesIO(current_position.read()), header=None, names=["ticker", "position"]
    )
    buy_recommends = buy_recommends.merge(position, how="left", on="ticker").fillna(
        {"position": 0}
    )

st.write(f"Found {buy_recommends.shape[0]} buy recommendations:")
st.dataframe(buy_recommends, hide_index=True, height=250)
