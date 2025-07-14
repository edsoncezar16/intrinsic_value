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
WHERE
    skipped IS NULL -- this filters out the metadata row added by dlt
