SELECT
    stock AS ticker,
    dividends,
    earnings,
    roe
FROM
    {{ source(
        'google_spreadsheet',
        'financial_info'
    ) }}
WHERE
    skipped IS NULL -- this filters out the metadata row added by dlt
