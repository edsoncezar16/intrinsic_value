import streamlit as st
from helpers import recommends

st.title("Buy Recommendations")

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

buy_recommends = recommends(margin_of_safety, "buy")

st.write(f"Found {buy_recommends.shape[0]} buy recommendations:")
st.dataframe(buy_recommends, hide_index=True)
