SELECT
    ticker,
    industry,
    company_name,
    market_price,
    market_price_date
FROM
    {{ source(
        'yfinance',
        'market_info'
    ) }}
