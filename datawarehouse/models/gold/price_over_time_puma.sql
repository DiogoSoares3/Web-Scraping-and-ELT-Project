{{ config(tags=['mercado_livre']) }}

WITH mercado_livre_filtered as (
    SELECT 
        name,
		reviews_rating_number as reviews_rating_mercado_livre,
        new_price as price_mercado_livre,
		datetime as datetime_mercado_livre
    FROM 
        {{ ref("stg-mercado_livre_tenis_corrida_masculino") }}
    WHERE 
        upper(brand) = 'PUMA'
),

puma_filtered as (
    SELECT 
        name,
        price as price_site_puma,
		datetime as datetime_site_puma
    FROM 
        {{ ref("stg-puma_tenis_corrida_masculino") }}
)

SELECT 
    l1.name,
	l1.datetime_mercado_livre,
	l2.datetime_site_puma,
    l2.price_site_puma,
    l1.price_mercado_livre,
    (l1.price_mercado_livre - l2.price_site_puma) as price_difference
FROM 
    mercado_livre_filtered l1
JOIN 
    puma_filtered l2 on upper(l1.name) = upper(l2.name)
