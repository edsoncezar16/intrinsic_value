SELECT
    1
FROM
    {{ ref('stg_google_sheets__model_params') }}
HAVING
    COUNT(*) != 1
