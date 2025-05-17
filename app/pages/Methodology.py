import streamlit as st

st.title("Methodology")

st.write(
    "Computes the intrinsic value of a company based on a two-stage discounted cash flow:"
)

st.markdown(
    """
1. First stage with a 10 years transient period with growth at the arithmetic mean between
   the terminal growth rate and the observed growth rate of the 5-year average net earnings
   over the last 10 years.

1. Steady-state with a terminal growth rate. This is taken to be the historical growth of the Brazilian
   economy. 
   For the data backing up this parameter, see: 
   `https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=BR`
"""
)

st.write("For the mathematically inclined reader, we have:")

st.latex(
    r"V = \bar{E}_0 \left[\sum_{i=1}^{10} \left(\frac{1 + \bar{\alpha}}{(1 + \gamma)}\right)^i + \left(1 + \bar{\alpha}\right)^{10}\frac{\left(1 + \alpha_\infty\right)}{\gamma - \alpha_\infty}\right],\,\bar{\alpha} = \frac{\alpha_0 + \alpha_\infty}{2}"
)
