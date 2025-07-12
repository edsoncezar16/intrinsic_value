SELECT
    stock,
    earnings :: FLOAT,
    dividends :: FLOAT,
    roe :: FLOAT
FROM
    {{ source(
        'google_sheets',
        'financial_data'
    ) }}
