import streamlit as st
from streamlit.connections import SQLConnection
from .config import QUERY_TTL, CONN_TTL_SECONDS


@st.cache_data(ttl=QUERY_TTL)
def get_total_companies(
    conn: SQLConnection = st.connection(
        name="intrinsic", type="sql", ttl=CONN_TTL_SECONDS
    ),
):
    return int(
        conn.query(
            """
            SELECT count(ticker) AS total_companies
            FROM main_analytics.intrinsic_value
            """,
            ttl=QUERY_TTL,
        )["total_companies"][0]
    )


@st.cache_data(ttl=QUERY_TTL)
def get_average_value(
    conn: SQLConnection = st.connection(
        name="intrinsic", type="sql", ttl=CONN_TTL_SECONDS
    ),
):
    avg_value = float(
        conn.query(
            """
            SELECT avg(intrinsic_value) AS average_value
            FROM main_analytics.intrinsic_value
            """,
            ttl=QUERY_TTL,
        )["average_value"][0]
    )
    return round(avg_value, 2)


@st.cache_data(ttl=QUERY_TTL)
def get_average_price(
    conn: SQLConnection = st.connection(
        name="intrinsic", type="sql", ttl=CONN_TTL_SECONDS
    ),
):
    avg_price = float(
        conn.query(
            """
            SELECT avg(market_price) AS average_price
            FROM main_analytics.intrinsic_value
            """,
            ttl=QUERY_TTL,
        )["average_price"][0]
    )
    return round(avg_price, 2)


@st.cache_data(ttl=QUERY_TTL)
def get_analysis_data(
    conn: SQLConnection = st.connection(
        name="intrinsic", type="sql", ttl=CONN_TTL_SECONDS
    ),
):
    return conn.query(
        """
            SELECT company_name, round(1.0 - market_price / intrinsic_value, 4) * 100 as discount
            FROM main_analytics.intrinsic_value
            WHERE intrinsic_value > 0.0
            """,
        ttl=QUERY_TTL,
    )
