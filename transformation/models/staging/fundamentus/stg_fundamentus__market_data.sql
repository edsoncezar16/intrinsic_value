SELECT
    ticker,
    -- Fixes inconsistencies at the source:
    ---- type 1: mismatch between company names scraped from the website and from the balance sheets
    ---- type 2: wrong stock type on website
    ---- type 3: company name contains "ON", which will conflict with scraping rules
    CASE
        WHEN company_name = 'CSNMINERACAO' THEN 'CSN MINERACAO' -- type 1
        WHEN company_name = 'COMPANHIA DE GÁS DE SÃO PAULO - COMGÁS' THEN 'COMPANHIA DE GÁS DE SÃO PAULO' -- type 1
        WHEN company_name = 'CYRELA BRAZIL REALTY PN' THEN 'CYRELA BRAZIL REALTY' -- type 2
        WHEN company_name = 'BANCO DA AMAZ' THEN 'BANCO DA AMAZONIA S.A.' -- type 3
        WHEN company_name = 'CIA ENERG CEARA - COELCE' THEN 'CIA ENERG CEARA' -- type 1
        WHEN company_name = 'OD' THEN 'ODONTOPREV' -- type 3
        WHEN company_name = 'PETROREC' THEN 'PETRORECONCA' -- type 3
        WHEN company_name = 'WILS' THEN 'WILSON SONS' -- type 3
        WHEN ticker = 'BMKS3' THEN 'MONARK' -- type 3
        WHEN ticker = 'MOAR3' THEN 'MONTEIRO ARANHA' -- type 3
        WHEN company_name = 'IOCHPE-MAXI' THEN 'IOCHPE-MAXION' -- type 1
        WHEN company_name = 'GUARARAPES C' THEN 'GUARARAPES CONFECÇÕES' -- type 3
        WHEN company_name = '' THEN 'ONCOCLINICAS' -- type 3
        ELSE company_name
    END AS company_name,
    industry,
    n_stocks,
    market_price,
    market_price_date
FROM
    {{ source(
        'fundamentus',
        'market_data'
    ) }}
