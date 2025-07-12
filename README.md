# Intrinsic

A data-driven app to construct value investing portfolios for the Brazilian Stock Exchange, grounded in the principle of **margin of safety**.

## Methodology

This application:

- Computes the **intrinsic value** of stocks using a two-stage **dividend discount model (DDM)**, as outlined in [*Corporate Finance (4th Edition)*](https://www.amazon.com/Corporate-Finance-Stephen-Ross/dp/0078034779) by Ross, Westerfield, and Jaffe.
- Calculates the **margin of safety** (MoS) as:

```latex
MoS = 1 - (market_price / intrinsic_value)
```

- **Filters for stocks with MoS > 50%**, signaling strong undervaluation relative to fundamentals.
- Assigns portfolio **weights using `2 * MoS - 1`**, emphasizing companies with higher safety margins.
- Accepts user input for **total capital**, and computes the number of shares to purchase per stock.

The result is a simple yet rigorous portfolio allocation strategy based on conservative valuation principles.

## Acknowledgements

The author wholeheartedly thanks the maintainers of the
[Fundamentus](https://www.fundamentus.com.br/index.php) website, which provides easy access to accurate
and up-to-date information on the fundamentals of Brazilian companies.
