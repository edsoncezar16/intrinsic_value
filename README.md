# Intrinsic

A data-driven app to construct value investing portfolios for the Brazilian Stock Exchange, grounded in the principle of **margin of safety**.

## Methodology

This application:

- Computes the **intrinsic value** of stocks using a **two-stage dividend discount model (DDM)**, based on the formulation in [*Corporate Finance (4th Edition)*](https://www.amazon.com/Corporate-Finance-Stephen-Ross/dp/0078034779) by Ross, Westerfield, and Jaffe.

- The model distinguishes two cases based on the implied growth rate `g = (1 - d/e) * ROE`:
  
  - If `g < gt` (terminal growth rate), the **Gordon Growth Model** is used:

    ```latex
        intrinsic_value = d * (1 + g) / (r - g)
    ```
  
  - If `g ≥ gt`, a **two-stage valuation** is applied:
    1. A 𝑛-year high-growth period with growing dividends discounted annually.
    2. A terminal value, adjusted by a **payout ratio scaling** to reflect convergence from the initial payout ratio `1 - g/ROE` to the terminal one `1 - gt/ROE`.

    ```latex
    payout_scale = (1 - gt/ROE) / (1 - g/ROE)
    adjusted_terminal_dividend = D_n * payout_scale
    terminal_value = adjusted_terminal_dividend * (1 + gt) / (r - gt)
    ```

- Computes the **margin of safety (MoS)**:

```latex
MoS = 1 - (market_price / intrinsic_value)
```

- Filters for stocks with **MoS > 50%**, favoring only deeply undervalued companies.

- Assigns portfolio weights as:

```latex
weight = 2 * MoS - 1
```

This ensures a zero weight at exactly 50% MoS, increasing linearly with higher safety margins.

- Accepts user input for **total capital**, and computes how many shares to buy per company based on price and portfolio weight.
