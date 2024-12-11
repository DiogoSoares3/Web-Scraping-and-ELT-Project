{{ config(tags=['mercado_livre', 'magalu', 'puma_site']) }}

WITH mercado_livre_filtered AS (
    SELECT 
        name,
        brand,
        new_price AS price,
        'mercado_livre' AS site
    FROM 
        {{ ref("stg-mercado_livre_tenis_corrida_masculino") }}
    WHERE 
        upper(brand) = 'PUMA'
),

puma_filtered AS (
    SELECT 
        name,
        'PUMA' AS brand,
        price,
        'puma_site' AS site
    FROM 
        {{ ref("stg-puma_tenis_corrida_masculino") }}
),

magalu_filtered AS (
    SELECT 
        name,
        CASE 
            WHEN upper(name) LIKE '% PUMA %' THEN 'PUMA'
            ELSE NULL
        END AS brand,
        new_price AS price,
        'magalu' AS site
    FROM 
        {{ ref("stg-magalu_tenis_corrida_masculino") }}
),

all_prices AS (
    SELECT * FROM mercado_livre_filtered
    UNION ALL
    SELECT * FROM puma_filtered
    UNION ALL
    SELECT * FROM magalu_filtered WHERE brand IS NOT NULL
)

SELECT 
    name,
    brand,
    price,
    site
FROM 
    all_prices
ORDER BY 
    price ASC
LIMIT 10
