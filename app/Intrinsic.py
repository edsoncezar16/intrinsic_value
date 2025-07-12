import streamlit as st

st.title("Intrinsic")

st.write(
    "A portfolio construction tool for value investing on the Brazilian Stock Exchange, based on the concept of margin of safety (MoS)."
)

st.header("Methodology")

st.markdown(
    """
    The app estimates the intrinsic value of stocks based on a **two-stage dividend discount model (DDM)**, as detailed in
    [*Corporate Finance (4th Edition), by Ross, Westerfield, and Jaffe*](https://www.amazon.com/Corporate-Finance-Stephen-Ross/dp/0078034779).
    
    Using intrinsic value estimates and market prices, we compute the **margin of safety (MoS)**:

    $$
    \\text{MoS} = 1 - \\frac{\\text{Market Price}}{\\text{Intrinsic Value}}
    $$

    A portfolio is constructed with the following logic:

    - **Only stocks with MoS > 50% are included**
    - **Portfolio weights are calculated as:**  
      $$
      \\text{Weight} = 2 \\times \\text{MoS} - 1
      $$
      Stocks with exactly 50% MoS receive zero weight. Higher MoS results in greater allocation.
    """
)

st.markdown(
    """
#### Valuation Formula

The intrinsic value formula used is:

$$
V = D_0 \\left[\\sum_{i=1}^{n} \\left(\\frac{1 + g}{1 + r}\\right)^i + \\left(\\frac{1 + g}{1 + r}\\right)^n \\left(\\frac{1 + g_t}{r - g_t}\\right)\\right]
$$

Where:

$$
\\def\\arraystretch{1.5}
\\begin{array}{:c:c:}
\\hdashline
V & \\text{Intrinsic Value}  \\\\
\\hdashline
D_0 & \\text{Current dividend}  \\\\
\\hdashline
g & \\text{Initial growth rate (e.g., ROE * retention)} \\\\
\\hdashline
g_t & \\text{Terminal growth rate} \\\\
\\hdashline
r & \\text{Required rate of return} \\\\
\\hdashline
n & \\text{Years of high growth period} \\\\
\\hdashline
\\end{array}
$$

If either `D_0` or earnings are negative, the intrinsic value is conservatively set to zero.
"""
)

st.markdown(
    """
#### Portfolio Construction Summary

- **Filter**: Stocks must have margin of safety greater than 50%
- **Weight formula**: `weight = 2 * MoS - 1`
- **Normalize weights** to sum to 1 across the portfolio

This creates a portfolio that leans heavily on companies with substantial undervaluation relative to their fundamentals.
"""
)

st.header("Acknowledgements")

st.markdown(
    """
    The author thanks the maintainers of
    [Fundamentus](https://www.fundamentus.com.br/index.php), which provides structured access to reliable
    fundamental data for Brazilian equities.
    """
)
