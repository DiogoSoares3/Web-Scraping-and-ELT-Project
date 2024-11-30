{{ config(tags=['mercado_livre', 'magalu', 'puma_site']) }}

WITH mercado_livre_filtered AS (
    SELECT 
        new_price AS price
    FROM 
        {{ ref("stg-mercado_livre_tenis_corrida_masculino") }}
    WHERE 
        upper(brand) = 'PUMA'
),

puma_filtered AS (
    SELECT 
        price
    FROM 
        {{ ref("stg-puma_tenis_corrida_masculino") }}
),

magalu_filtered AS (
    SELECT 
        CASE 
            WHEN upper(name) LIKE '% PUMA %' THEN 'PUMA'
            ELSE NULL
        END AS brand,
        new_price AS price
    FROM 
        {{ ref("stg-magalu_tenis_corrida_masculino") }}
),

statistics_metrics AS (
    SELECT
        'mercado_livre' as site,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        AVG(price) AS mean_price,
        STDDEV(price) AS stddev_price,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS percentile_25,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median_price,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS percentile_75,
        COUNT(*) AS qtd_shoes
    FROM 
        mercado_livre_filtered
    WHERE 
        price IS NOT NULL

    UNION ALL

    SELECT
        'puma_site' as site,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        AVG(price) AS mean_price,
        STDDEV(price) AS stddev_price,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS percentile_25,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median_price,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS percentile_75,
        COUNT(*) AS qtd_shoes
    FROM 
        puma_filtered
    WHERE 
        price IS NOT NULL

    UNION ALL

    SELECT
        'magalu' as site,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        AVG(price) AS mean_price,
        STDDEV(price) AS stddev_price,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS percentile_25,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median_price,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS percentile_75,
        COUNT(*) AS qtd_shoes
    FROM 
        magalu_filtered
    WHERE 
        brand = 'PUMA' AND price IS NOT NULL
)

SELECT * FROM statistics_metrics
