WITH base AS (
    SELECT
        ticker,
        company_name,
        industry,
        ROUND(
            {{ compute_intrinsic_value(
                d = 'dividends',
                e = 'earnings',
                roe = 'roe',
                r = var('risk_free_rate'),
                gt = var('terminal_growth_rate'),
                n = var('transient_period')
            ) }},
            2
        ) AS intrinsic_value,
        market_price,
        market_price_date AS as_of
    FROM
        {{ ref('stg_google_sheets__financial_info') }}
        JOIN {{ ref('stg_yfinance__market_info') }} USING ticker
)
SELECT
    ticker,
    company_name,
    industry,
    intrinsic_value,
    market_price,
    CASE
        WHEN intrinsic_value > 0 THEN (
            intrinsic_value - market_price
        ) / intrinsic_value
        ELSE NULL
    END AS margin_of_safety,
    as_of
FROM
    base
