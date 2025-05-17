import duckdb
import streamlit as st


@st.cache_data
def recommends(margin_of_safety, kind):
    if kind == "buy":
        filter_condition = (
            f"WHERE market_price < intrinsic_value  * {1.0 - margin_of_safety}"
        )
    elif kind == "sell":
        filter_condition = (
            f"WHERE market_price > intrinsic_value * {1.0 + margin_of_safety}"
        )
    else:
        raise ValueError("Recommendation kind should be one of 'buy' or 'sell'.")

    with duckdb.connect("../intrinsic.duckdb") as con:
        data = con.execute(
            f"""
            SELECT * 
            FROM main_analytics.intrinsic_value
            {filter_condition}
            ORDER BY intrinsic_value {"DESC" if kind == "buy" else ""} 
            """
        ).fetch_df()
    return data
