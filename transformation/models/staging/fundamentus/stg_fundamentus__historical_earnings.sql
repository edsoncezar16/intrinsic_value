SELECT
    -- Fixes inconsistencies at the source:
    ---- type 1: mismatch between company names scraped from the website and from the balance sheets
    ---- type 2: wrong stock type on website
    ---- type 3: company name contains "ON", which will conflict with scraping rules
    CASE
        WHEN company_name = 'IOCHPE' THEN 'IOCHPE-MAXION' -- type 1
        WHEN company_name = 'FRAS' THEN 'FRAS-LE S.A.' -- type 1
        WHEN company_name = 'CEB' THEN 'CEB - COMPANHIA ENERGÉTICA DE BRASÍLIA' -- type 1
        WHEN company_name = 'Log' THEN 'Log-In' -- type 1
        WHEN company_name = 'QUERO' THEN 'QUERO-QUERO'
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
