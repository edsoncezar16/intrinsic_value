import streamlit as st

st.title("Intrinsic")

st.write(
    "A data app to support value investing decisions in the Brazilian Stock Exchange."
)


st.header("Methodology")


st.markdown(
    """
    Computes the **earnings power of a company**, defined as the **average earnings over the last 10 years divided by its current price**, and recommends buying when there is a **margin of safety** of at least 50% as compared to the yield on long-term government bond.

    For a deep dive on the above concepts, we recommend the reading of [The Intelligent Investor](https://www.amazon.com/Intelligent-Investor-Definitive-Investing-Essentials/dp/0060555661) (especially Chapter 20).
    """
)

st.header("Acknowledgements")

st.markdown(
    """
    The author wholeheartedly thanks the maintainers of the
    [Fundamentus](https://www.fundamentus.com.br/index.php) website, which provides easy access to accurate
    and up to date information of the underlying fundamentals of Brazilian companies.
    """
)
