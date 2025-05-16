SELECT
    company_name,
    list_aggregate(
        earnings_history [1:20],
        'sum'
    ) AS past_5yr_earnings,
    list_aggregate(
        earnings_history [-20:-1],
        'sum'
    ) AS current_5yr_earnings
FROM
    {{ ref('stg_fundamentus__historical_earnings') }}
