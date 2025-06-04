import streamlit as st
from streamlit.connections import SQLConnection
from .config import QUERY_TTL, CONN_TTL_SECONDS


@st.cache_data(ttl=QUERY_TTL)
def recommends(
    kind: str,
    margin_of_safety: float = 0.5,
    conn: SQLConnection = st.connection(
        name="intrinsic", type="sql", ttl=CONN_TTL_SECONDS
    ),
):
    if kind == "buy":
        filter_condition = (
            f"WHERE market_price < intrinsic_value  * {1.0 - margin_of_safety}"
        )
    elif kind == "sell":
        filter_condition = "WHERE market_price > intrinsic_value"
    else:
        raise ValueError("Recommendation kind should be one of 'buy' or 'sell'.")

    return conn.query(
        f"""
            SELECT * 
            FROM main_analytics.intrinsic_value
            {filter_condition}
            ORDER BY intrinsic_value DESC 
            """,
        ttl=QUERY_TTL,
    )
