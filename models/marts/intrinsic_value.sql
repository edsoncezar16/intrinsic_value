SELECT
    company_name,
    {{ compute_intrinsic_value(
        past_5yr_net_earnings = 'past_5yr_earnings',
        current_5yr_net_earnings = 'current_5yr_earnings',
        risk_free_rate = var('risk_free_rate'),
        terminal_growth_rate = var('terminal_growth_rate')
    ) }} * 1000 AS intrinsic_value
FROM
    {{ ref('prepared_historical_earnings') }}
