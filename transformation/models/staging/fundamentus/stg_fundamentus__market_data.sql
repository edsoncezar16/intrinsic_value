SELECT
    ticker,
    CASE
        WHEN company_name = 'CSNMINERACAO' THEN 'CSN MINERACAO'
        WHEN company_name = 'COMPANHIA DE GÁS DE SÃO PAULO - COMGÁS' THEN 'COMPANHIA DE GÁS DE SÃO PAULO'
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
