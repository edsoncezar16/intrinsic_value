# Intrinsic

A data app that allows one to assess the intrinsic value of a company from the Brazilian stock exchange
based on its historical performance, expected long-term growth rate, and discount rate.

## Methodology

Computes the intrinsic value of a company based on a two-stage discounted cash flow,
as outlined in the book [The Warren Buffet Way](https://www.amazon.com/Warren-Buffett-Way-Third/dp/1118819233).

1. First stage with a 10 years transient period with growth at the arithmetic mean between
   the terminal growth rate and the observed growth rate of the 5-year average net earnings
   over the last 10 years.

1. Steady-state with a terminal growth rate. This is taken to be the historical growth of the Brazilian
   economy. For the data backing up this parameter, see:
   `https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=BR`

## Acknowledgements

The author wholeheartedly thanks the maintainers of the
[Fundamentus](https://www.fundamentus.com.br/index.php) website, which provides easy access to accurate
and up to date information of the underlying fundamentals of Brazilian companies.

## Notes on data availability

From all the `289` companies listed at B3, we **don't cover** the following `5`due to
data being unavailable in some form as to make the analysis unfeasible:

- CIABRASF (ADMF3)
- RDVC CITY (CCTY3)
- REVEE (RVEE3)
- IRB(RE) (IRBR3)
- SANSUY (SNSY3)
