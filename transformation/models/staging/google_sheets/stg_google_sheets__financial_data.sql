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
        'google_sheets',
        'financial_data'
    ) }}
