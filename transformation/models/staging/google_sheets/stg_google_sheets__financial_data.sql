SELECT
    stock,
    CAST(
        dividends AS FLOAT
    ),
    CAST(
        earnings AS FLOAT
    ),
    CAST(
        roe AS FLOAT
    )
FROM
    {{ source(
        'trading_view',
        'financial_info'
    ) }}
