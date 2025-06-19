SELECT
    company_name,
    list_aggregate(
        earnings_history [-40:-1],
        'sum'
    ) / 10 AS avg_10yr_earnings,
FROM
    {{ ref('stg_fundamentus__historical_earnings') }}
