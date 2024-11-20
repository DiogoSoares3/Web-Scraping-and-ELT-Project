-- import

WITH source as (
    SELECT DISTINCT ON ("name", "old_price", "new_price", "rating_and_number_of_evaluations", "discount_pix")
        "name",
        "old_price",
        "new_price",
        "rating_and_number_of_evaluations",
        "discount_pix",
        "datetime"
    FROM 
        {{source ("WebScraping", "raw-magalu_tenis_corrida_masculino")}}  
),

-- renamed

renamed as (
    SELECT -- ARRUMAR ESSE REPLACE DO R$
        cast("name" as text),
        cast(replace(replace("old_price", ',', '.'), 'R$ ', '') as float) as old_price,
        cast(replace(replace("new_price", ',', '.'), 'R$ ', '') as float) as new_price,
        cast(substring("rating_and_number_of_evaluations" FROM '^[0-9.]+') as float) as rating,
        cast(substring("rating_and_number_of_evaluations" FROM '\((\d+)\)') as float) as number_of_evaluations,
        substring('discount_pix' FROM '(\d+%)') AS descount_pix,
        to_timestamp(cast("datetime" as float)) as datetime
    FROM source
)

SELECT * FROM renamed