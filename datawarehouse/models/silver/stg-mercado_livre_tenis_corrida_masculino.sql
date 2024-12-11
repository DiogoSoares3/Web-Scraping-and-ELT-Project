{{ config(tags=['mercado_livre']) }}

-- import

WITH source as (
    SELECT DISTINCT ON (
        "brand", "name", "old_price_reais",
        "old_price_cents","new_price_reais","new_price_cents",
        "reviews_rating_number", "reviews_amount")

        "id",
        "brand",
        "name",
        "old_price_reais",
        "old_price_cents",
        "new_price_reais",
        "new_price_cents",
        "reviews_rating_number",
        "reviews_amount",
        "datetime"
    FROM 
        {{source ("WebScraping", "raw-mercado_livre_tenis_corrida_masculino")}}  
),

-- renamed

renamed as (
    SELECT
        "id",
        cast("brand" as text),
        cast("name" as text),
        cast(replace("old_price_reais", '.', '') || '.' || "old_price_cents" as float) as old_price,
        cast(replace("new_price_reais", '.', '') || '.' || "new_price_cents" as float) as new_price,
        cast("reviews_rating_number" as float),
        cast(replace(replace("reviews_amount", '(', ''), ')', '') as integer) as reviews_amount,
        to_timestamp(cast("datetime" as float)) as datetime
    FROM source
)

SELECT * FROM renamed
