SELECT
    discount_rate,
    terminal_growth_rate,
    transient_period
FROM
    {{ source(
        'google_sheets',
        'model_params'
    ) }}
