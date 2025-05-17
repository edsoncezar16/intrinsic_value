import streamlit as st
from helpers import recommends

st.title("Buy Recommendations")

margin_of_safety = st.slider(
    "Enter you desired margin of safety: ", min_value=0.0, max_value=1.0, value=0.2
)

st.dataframe(recommends(margin_of_safety, "buy"), hide_index=True)
