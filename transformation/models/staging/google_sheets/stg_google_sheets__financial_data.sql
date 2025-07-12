SELECT
    stock,
    dividends,
    earnings,
    roe
FROM
    {{ source(
        'trading_view',
        'financial_info'
    ) }}
WHERE
    skipped IS NULL -- this filters out the metadata row added by dlt
