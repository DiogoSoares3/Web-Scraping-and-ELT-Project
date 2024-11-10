-- import

with source as (
    select 
        "brand",
        "name",
        "old_price_reais",
        "old_price_cents",
        "new_price_reais",
        "new_price_cents",
        "reviews_rating_number",
        "reviews_amount",
        "datetime"
    from 
        {{source ("WebScraping", "mercado_livre_tenis-corrida-masculino")}}  
),

-- renamed

renamed as (
    select
        cast("brand" as text),
        cast("name" as text),
        cast("old_price_reais" || '.' || "old_price_cents" as float) as old_price, --- Fazer CASE THEN, pois tem old_price que tem o preço junto com centavo já
        cast("new_price_reais" || '.' || "new_price_cents" as float) as new_price,
        cast("reviews_rating_number" as float),
        cast(replace(replace("reviews_amount", '(', ''), ')', '') as integer) as reviews_amount,
        to_timestamp(cast("datetime" as float)) as datetime
    from source
)

select * from renamed