import streamlit as st
from helpers import recommends
import plotly.express as px
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

sell_recommends = recommends("sell")

if current_position:
    position = pd.read_csv(
        BytesIO(current_position.read()), header=None, names=["ticker", "position"]
    )
    sell_recommends = sell_recommends.merge(position, how="left", on="ticker").fillna(
        {"position": 0}
    )

st.write(f"Found {sell_recommends.shape[0]} sell recommendations:")
st.dataframe(sell_recommends, hide_index=True, height=250)

industry_distribution = sell_recommends.groupby("industry").agg({"ticker": "count"})
industry_distribution.columns = ["N. Companies"]
plotted_industry_distribution = industry_distribution.sort_values("N. Companies").tail(
    5
)

fig = px.bar(
    plotted_industry_distribution,
    y=plotted_industry_distribution.index,
    x="N. Companies",
    orientation="h",
    title="Top 5 Industries in Sell Recommendations",
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
