WITH base AS (
    SELECT
        f.ticker,
        f.company_name,
        m.industry,
        ROUND(
            {{ compute_intrinsic_value(
                d = 'dividends',
                e = 'earnings',
                roe = 'roe',
                r = 'discount_rate',
                gt = 'terminal_growth_rate',
                n = 'transient_period'
            ) }},
            2
        ) AS intrinsic_value,
        m.market_price,
        m.market_price_date AS as_of
    FROM
        {{ ref('stg_google_sheets__financial_info') }}
        f
        LEFT JOIN {{ ref('stg_yfinance__market_info') }}
        m
        ON f.ticker = m.ticker
        CROSS JOIN {{ ref('stg_google_sheets__model_params') }}
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
