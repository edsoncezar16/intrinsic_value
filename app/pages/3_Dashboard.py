import streamlit as st
from helpers import (
    get_analysis_data,
    get_average_price,
    get_average_value,
    get_total_companies,
)
import plotly.express as px

st.title("Dashboard")

st.header("Big Numbers")
a, b, c = st.columns(3)
a.metric("Total Companies Covered", get_total_companies())
b.metric("Average Market Price", get_average_price())
c.metric("Average Intrinsic Value", get_average_value())

analysis_data = get_analysis_data()

st.header("Bargain Companies")

plotted_bargain = (
    analysis_data.rename(columns={"discount": "discount (%)"})
    .sort_values("discount (%)")
    .tail(5)
    .set_index("company_name")
)

value_fig = px.bar(
    plotted_bargain,
    y=plotted_bargain.index,
    x="discount (%)",
    title="Top 5 Companies by Discount from Intrinsic Value",
    height=40 * len(plotted_bargain),
)

value_fig.update_layout(
    yaxis=dict(
        tickmode="array",
        tickvals=plotted_bargain.index,
    ),
    margin=dict(l=150, r=20, t=50, b=50),
)

st.plotly_chart(value_fig)


st.header("Overpriced Companies")

plotted_overpriced = (
    analysis_data.set_index("company_name")
    .map(lambda x: -x)
    .rename(columns={"discount": "excess (%)"})
    .sort_values("excess (%)")
    .tail(5)
)

value_fig = px.bar(
    plotted_overpriced,
    y=plotted_overpriced.index,
    x="excess (%)",
    title="Top 5 Companies by Excess over Intrinsic Value",
    height=40 * len(plotted_overpriced),
)

value_fig.update_layout(
    yaxis=dict(
        tickmode="array",
        tickvals=plotted_overpriced.index,
    ),
    margin=dict(l=150, r=20, t=50, b=50),
)

st.plotly_chart(value_fig)
