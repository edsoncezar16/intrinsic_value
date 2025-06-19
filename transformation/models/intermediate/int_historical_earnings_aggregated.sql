SELECT
    company_name,
    list_aggregate(
        earnings_history [-40:-1],
        'sum'
    ) AS past_10yr_earnings,
FROM
    {{ ref('stg_fundamentus__historical_earnings') }}
