
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

magalu_filtered as (
    SELECT 
        name,
        new_price as price_magalu,
		datetime as datetime_magalu
    FROM 
        {{ ref("stg-magalu_tenis_corrida_masculino") }}
    WHERE
        upper(name) like '% PUMA %'  
)

SELECT 
    l1.name,
    l1.datetime_mercado_livre,
    l2.datetime_site_puma,
    l3.datetime_magalu,
    l2.price_site_puma,
    l1.price_mercado_livre,
    l3.price_magalu,
    least(l1.price_mercado_livre, l2.price_site_puma, l3.price_magalu) as best_price,
    CASE 
        WHEN least(l1.price_mercado_livre, l2.price_site_puma, l3.price_magalu) = l1.price_mercado_livre THEN 'mercado_livre'
        WHEN least(l1.price_mercado_livre, l2.price_site_puma, l3.price_magalu) = l2.price_site_puma THEN 'site_puma'
        WHEN least(l1.price_mercado_livre, l2.price_site_puma, l3.price_magalu) = l3.price_magalu THEN 'magalu'
    END as source
FROM 
    mercado_livre_filtered l1
JOIN 
    puma_filtered l2 
    ON upper(l1.name) = upper(l2.name)
JOIN 
    magalu_filtered l3 
    ON upper(l1.name) = upper(l3.name)
ORDER BY 
    best_price ASC
LIMIT 10;

-- ARRUMAR O JOIN DO name DA MAGALU