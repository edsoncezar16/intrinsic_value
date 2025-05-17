# Intrinsic

A data app that allows one to assess the intrinsic value of a company from the Brazilian stock exchange
based on its historical performance, expected long-term growth rate, and discount rate.

## Methodology

Computes the intrinsic value of a company based on a two-stage discounted cash flow:

1. First stage with a 10 years transient period with growth at the arithmetic mean between
   the terminal growth rate and the observed growth rate of the 5-year average net earnings
   over the last 10 years.

1. Steady-state with a terminal growth rate. This is taken to be the historical growth of the Brazilian
   economy. For the date backing up this parameter, see:
   `https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG?locations=BR`

## TODO

- Let user define margin of safety in the app and return all companies below the margin of safety (buy recommends by default)
- Set option to get sell recommends.
