SELECT
    ticker,
    industry,
    company_name,
    ROUND(
        market_price,
        2
    ),
    market_price_date
FROM
    {{ source(
        'yfinance',
        'market_info'
    ) }}
