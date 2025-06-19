SELECT
    ticker,
    e.company_name,
    industry,
    -- factor of 1000 is to reconcile earnings expressed in thousands of R$
    -- so we should divide by the stocks in thousands of units
    ROUND(
        avg_10yr_earnings / market_price * 1000 / n_stocks,
        2
    ) AS earnings_power,
    market_price,
    market_price_date AS as_of
FROM
    {{ ref('int_historical_earnings_aggregated') }}
    e
    LEFT JOIN {{ ref('int_market_data_industry_translated') }}
    m
    ON m.company_name = e.company_name
