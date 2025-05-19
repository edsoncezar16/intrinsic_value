import streamlit as st
from streamlit.connections import SQLConnection

# should be set to '1d' after development is done
QUERY_TTL_SECONDS = 30.0

CONN_TTL_SECONDS = 60.0


@st.cache_data(ttl=QUERY_TTL_SECONDS)
def recommends(
    margin_of_safety: float,
    kind: str,
    conn: SQLConnection = st.connection(
        name="intrinsic", type="sql", ttl=CONN_TTL_SECONDS
    ),
):
    if kind == "buy":
        filter_condition = (
            f"WHERE market_price < intrinsic_value  * {1.0 - margin_of_safety}"
        )
    elif kind == "sell":
        filter_condition = f"WHERE market_price > intrinsic_value * {1.0 + margin_of_safety} OR intrinsic_value IS NULL"
    else:
        raise ValueError("Recommendation kind should be one of 'buy' or 'sell'.")

    return conn.query(
        f"""
            SELECT * 
            FROM main_analytics.intrinsic_value
            {filter_condition}
            ORDER BY intrinsic_value {"DESC" if kind == "buy" else ""} 
            """,
        ttl=QUERY_TTL_SECONDS,
    )
