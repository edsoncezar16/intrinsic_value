SELECT
    ticker,
    company_name,
    industry_en AS industry,
    n_stocks,
    market_price,
    market_price_date
FROM
    {{ ref(
        'stg_fundamentus__market_data'
    ) }}
    m
    LEFT JOIN {{ ref('industry_translation') }}
    t
    ON m.industry = t.industry_pt
