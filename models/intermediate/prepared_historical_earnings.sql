WITH raw_historical_earnings AS (
    SELECT
        company_name,
        CAST(
            VALUES
                -> '$[*]' AS DOUBLE []
        ) AS earnings_history
    FROM
        {{ source(
            'fundamentus',
            'historical_earnings'
        ) }}
)
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
    raw_historical_earnings
