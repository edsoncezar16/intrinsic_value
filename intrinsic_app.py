import streamlit as st
import duckdb

st.title("Instrinsic")

st.write("Instrinsic value of companies in the Brazilian stock exchange.")

@st.cache_data
def load_data(nrows, like_param = ""):
    with duckdb.connect("fundamentus_pipeline.duckdb") as con:
        filter_condition = f"WHERE company_name LIKE {like_param}" if like_param else ""
        data = con.execute(
            f"""
            SELECT * 
            FROM intrinsic_value
            {filter_condition} 
            ORDER BY intrinsic_value DESC 
            LIMIT {nrows}
            """
        )
    return data.fetch_df()

n_stocks = st.slider("Number of Stocks to Visualize", min_value=1, step=1, value=15)

like_param = st.text_input("Filter company name like: ")

st.dataframe(load_data(n_stocks, like_param=like_param))