SELECT
    1
FROM
    {{ source(
        'google_sheets',
        'model_params'
    ) }}
HAVING
    COUNT(*) != 1
