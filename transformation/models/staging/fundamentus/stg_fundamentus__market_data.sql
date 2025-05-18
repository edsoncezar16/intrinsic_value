SELECT
    ticker,
    -- Fixes inconsistencies at the source:
    ---- type 1: mismatch between company names scraped from the website and from the balance sheets
    ---- type 2: wrong stock type on website
    CASE
        WHEN company_name = 'CSNMINERACAO' THEN 'CSN MINERACAO' -- type 1
        WHEN company_name = 'COMPANHIA DE GÁS DE SÃO PAULO - COMGÁS' THEN 'COMPANHIA DE GÁS DE SÃO PAULO' -- type 1
        WHEN company_name = 'CYRELA BRAZIL REALTY PN' THEN 'CYRELA BRAZIL REALTY' -- type 2
        ELSE company_name
    END AS company_name,
    n_stocks,
    market_price,
    market_price_date
FROM
    {{ source(
        'fundamentus',
        'market_data'
    ) }}
