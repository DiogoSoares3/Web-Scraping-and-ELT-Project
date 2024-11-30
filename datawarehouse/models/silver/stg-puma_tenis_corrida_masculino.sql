{{ config(tags=['puma_site']) }}

-- import

WITH source AS (
    SELECT DISTINCT ON ("name", "price", "label", "ultimos_tamanhos")
        "id",
        "name",
        "price",
        "label",
        "ultimos_tamanhos",
        "datetime"
    FROM 
        {{source ("WebScraping", "raw-puma_tenis_corrida_masculino")}}
),

--renamed

renamed as (
	SELECT
        "id",
		'Puma' as brand,
		cast("name" as text),
		cast(replace(replace(replace("price", 'R$', ''), '.', ''), ',', '.') as float) as price,
		cast("label" as text),
		cast("ultimos_tamanhos" as boolean) as last_sizes,
		to_timestamp(cast("datetime" as float)) as datetime
	FROM source
)

SELECT * FROM renamed

-- PROXIMA ETAPA: Tratar dados duplicados aqui na camada Silver