import streamlit as st
from helpers import recommends
import pandas as pd
import plotly.express as px
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
    "Enter you desired margin of safety: ", min_value=0.1, max_value=0.5, value=0.2
)

buy_recommends = recommends(margin_of_safety, "buy")


if current_position:
    position = pd.read_csv(
        BytesIO(current_position.read()), header=None, names=["ticker", "position"]
    )
    buy_recommends = buy_recommends.merge(position, how="left", on="ticker")

st.write(f"Found {buy_recommends.shape[0]} buy recommendations:")
st.dataframe(buy_recommends, hide_index=True, height=250)

industry_distribution = buy_recommends.groupby("industry").agg({"ticker": "count"})
industry_distribution.columns = ["N. Companies"]
plotted_industry_distribution = industry_distribution.sort_values("N. Companies").tail(
    5
)

fig = px.bar(
    plotted_industry_distribution,
    y=plotted_industry_distribution.index,
    x="N. Companies",
    title="Top 5 Industries in Buy Recommendations",
    height=40 * len(plotted_industry_distribution),
)

fig.update_layout(
    yaxis=dict(
        tickmode="array",
        tickvals=plotted_industry_distribution.index,
    ),
    margin=dict(l=150, r=20, t=50, b=50),
)

st.plotly_chart(fig)
