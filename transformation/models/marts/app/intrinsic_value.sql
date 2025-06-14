WITH base AS (
    SELECT
        ticker,
        company_name,
        industry,
        -- factor of 1000 is to reconcile earnings expressed in thousands of R$
        -- so we should divide by the stocks in thousands of units
        ROUND(
            {{ compute_intrinsic_value(
                past_5yr_net_earnings = 'past_5yr_earnings',
                current_5yr_net_earnings = 'current_5yr_earnings',
                risk_free_rate = var('risk_free_rate'),
                terminal_growth_rate = var('terminal_growth_rate')
            ) }} * 1000 / n_stocks,
            2
        ) AS intrinsic_value,
        market_price,
        market_price_date AS as_of
    FROM
        {{ ref('int_historical_earnings_aggregated') }}
        LEFT JOIN {{ ref('int_market_data_industry_translated') }} USING (company_name)
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
    END AS margin_of_safety as_of
FROM
    baseS
