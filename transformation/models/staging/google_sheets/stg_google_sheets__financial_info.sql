SELECT
    stock AS ticker,
    dividends,
    earnings,
    roe
FROM
    {{ source(
        'google_sheets',
        'financial_info'
    ) }}
