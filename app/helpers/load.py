import streamlit as st
from streamlit.connections import SQLConnection
from .config import QUERY_TTL, CONN_TTL_SECONDS


@st.cache_data(ttl=QUERY_TTL)
def portfolio_data(
    conn: SQLConnection = st.connection(
        name="intrinsic", type="sql", ttl=CONN_TTL_SECONDS
    ),
):
    return conn.query(
        """
            SELECT * 
            FROM main_analytics.intrinsic_value
            WHERE margin_of_safety > 0.5
            ORDER BY margin_of_safety DESC 
            """,
        ttl=QUERY_TTL,
    )
