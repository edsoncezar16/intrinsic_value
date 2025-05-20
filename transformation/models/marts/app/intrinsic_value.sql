SELECT
    ticker,
    company_name,
    industry,
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
