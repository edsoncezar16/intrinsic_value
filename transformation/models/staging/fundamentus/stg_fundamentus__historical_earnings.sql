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