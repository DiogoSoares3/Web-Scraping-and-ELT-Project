-- {{ config(tags=['mercado_livre']) }}

WITH mercado_livre_filtered AS (
    SELECT 
        name,
        'mercado_livre' AS site,
        new_price AS price,
        datetime
    FROM 
        {{ ref("stg-mercado_livre_tenis_corrida_masculino") }}
    WHERE 
        upper(brand) = 'PUMA' AND upper(name) LIKE '% INFUSION %'
),

puma_filtered AS (
    SELECT 
        name,
        'site_puma' AS site,
        price,
        datetime
    FROM 
        {{ ref("stg-puma_tenis_corrida_masculino") }}
    WHERE 
        upper(name) LIKE '% INFUSION %'
),

magalu_filtered AS (
    SELECT 
        name,
        'magalu' AS site,
        new_price AS price,
        datetime
    FROM 
        {{ ref("stg-magalu_tenis_corrida_masculino") }}
    WHERE 
        upper(name) LIKE '% PUMA %' and upper(name) LIKE '% INFUSION %'
),

all_prices AS (
    SELECT * FROM mercado_livre_filtered
    UNION ALL
    SELECT * FROM puma_filtered
    UNION ALL
    SELECT * FROM magalu_filtered
)

SELECT 
    name,
    price,
    site,
    datetime
FROM 
    all_prices
ORDER BY 
    name, datetime, site

-- SUGESTÃO: Gráfico Eixo X: datetime, Eixo Y: price, Cor/linha: site
-- Vai permitir comparar os preços de um determinado modelo entre os sites ao longo do tempo de forma clara.
