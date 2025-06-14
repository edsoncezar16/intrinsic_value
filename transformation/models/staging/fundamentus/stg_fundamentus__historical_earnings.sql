SELECT
    -- Fixes inconsistencies at the source: company name contains "-",
    -- which will conflict with balance sheet parsing rules
    CASE
        WHEN company_name = 'IOCHPE' THEN 'IOCHPE-MAXION'
        WHEN company_name = 'FRAS' THEN 'FRAS-LE S.A.'
        WHEN company_name = 'CEB' THEN 'CEB - COMPANHIA ENERGÉTICA DE BRASÍLIA'
        WHEN company_name = 'Log' THEN 'Log-In'
        WHEN company_name = 'QUERO' THEN 'QUERO-QUERO'
        WHEN company_name = 'CEEE' THEN 'CEEE-D'
        WHEN company_name = 'ATMASA' THEN 'CONTAX'
        ELSE company_name
    END AS company_name,
    CAST(
        VALUES
            -> '$[*]' AS DOUBLE []
    ) AS earnings_history
FROM
    {{ source(
        'fundamentus',
        'historical_earnings'
    ) }}
