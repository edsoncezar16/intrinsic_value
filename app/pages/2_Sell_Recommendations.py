import streamlit as st
from helpers import recommends

st.title("Sell Recommendations")

st.warning(
    """
    Take the following list at most as a starting point for you own analysis.
    
    Every investment decision should be thoughtful and you are the sole responsible for them.  
    """,
    icon="⚠️",
)

margin_of_safety = st.slider(
    "Enter you desired margin of safety: ", min_value=0.1, max_value=0.5, value=0.2
)

sell_recommends = recommends(margin_of_safety, "sell")

st.write(f"Found {sell_recommends.shape[0]} sell recommendations:")
st.dataframe(sell_recommends, hide_index=True)
