import streamlit as st

st.title("Intrinsic")

st.write(
    "Instrinsic value of companies in the Brazilian stock exchange to support investments decisions."
)


st.header("Methodology")


st.markdown(
    """
    Computes the intrinsic value of a company based on a two-stage discounted cash flow,
    as outlined in the section *Value Tenets* from the book [The Warren Buffet Way](https://www.amazon.com/Warren-Buffett-Way-Third/dp/1118819233). 
    """
)

st.markdown(
    """
1. First stage with a 10 years transient period with a growth rate of the arithmetic mean between
   the terminal growth rate and the observed growth rate of the 5-year average net earnings
   over the last 10 years.

1. Steady-state with a terminal growth rate. This is taken to be the historical growth of the Brazilian
   economy. 
   For the data backing up this parameter, see: 
   `https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=BR`

*Note: if either average earnings is negative, we set intrinsic_value = 0.0*.
"""
)

st.write("For the mathematically inclined reader, we have:")

st.latex(
    r"""
    V = \bar{E}_0 \left[\sum_{i=1}^{10} \left(\frac{1 + \bar{\alpha}}{1 + \gamma}\right)^i + \left(1 + \bar{\alpha}\right)^{10}\frac{\left(1 + \alpha_\infty\right)}{\gamma - \alpha_\infty}\right],\space \bar{\alpha} = \frac{\alpha_0 + \alpha_\infty}{2}
    """
)
st.write("where:")
st.latex(
    r"""
    \def\arraystretch{1.5}
    \begin{array}{:c:c:}
   \hdashline
    V & \text{Intrinsic Value.}  \\ 
    \hdashline
    \bar{E}_0 & \text{Average net earnings over the last 5 years.}  \\
    \hdashline
    \alpha_0 & \text{Observed growth rate of the average net earnings over the last 10 years.}\\
    \hdashline
    \alpha_\infty & \text{Terminal growth rate of net earnings after the transient period.}\\
    \hdashline
    \gamma & \text{Interest rate for cash flow discount.}\\
    \hdashline
    \end{array}
    """
)

st.markdown(
    """
    Based on the previous computation and the concept of margin of safety, 
    we compute buy and sell recommendations as follows:
    
    - Buy Recommendations: market_price < (1 - margin_of_safety) * intrinsic_value
    - Sell Recommendations: market_price > (1 + margin_of_safety) * intrinsic_value
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
