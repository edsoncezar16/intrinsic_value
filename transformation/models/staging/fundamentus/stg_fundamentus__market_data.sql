SELECT
    *
FROM
    {{ source(
        'fundamentus',
        'market_data'
    ) }}
