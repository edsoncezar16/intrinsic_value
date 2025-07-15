SELECT
    stock AS ticker,
    company AS company_name,
    dividends,
    earnings,
    roe
FROM
    {{ source(
        'google_sheets',
        'financial_info'
    ) }}
