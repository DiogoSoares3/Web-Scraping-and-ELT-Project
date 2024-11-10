import scrapy
from datetime import datetime


class MercadoLivreTenisCorridaMasculinoSpider(scrapy.Spider):
    name = "mercado_livre_tenis-corrida-masculino"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]

    ## Execute 'scrapy shell' and explore the html content of the URL above
    ## When you test and get the results you want, put this in the fuction below:
    def parse(self, response):
        shoes_data = response.css('div.poly-card__content')
        
        if shoes_data == []:
            shoes_data = response.css('div.ui-search-result__content')
            
            for shoes_content in shoes_data:
                
                prices = shoes_content.css('span.andes-money-amount__fraction::text').getall()
                price_cents = shoes_content.css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-16::text').getall()

                yield {
                    "brand": shoes_content.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                    "name": shoes_content.css('a.ui-search-link__title-card.ui-search-link::text').get(),
                    "old_price_reais": prices[0] if len(prices) >= 2 else None,
                    "old_price_cents": price_cents[0] if len(price_cents) >= 2 else None,
                    "new_price_reais": prices[1] if len(prices) >= 2 else None,
                    "new_price_cents": price_cents[1] if len(price_cents) >= 2 else None,
                    "reviews_rating_number": shoes_content.css('span.ui-search-reviews__rating-number::text').get(),
                    "reviews_amount": shoes_content.css('span.ui-search-reviews__amount::text').get(),
                    "datetime": datetime.now().timestamp()
                }
            
        else:
            for shoes_content in shoes_data:
                
                prices = shoes_content.css('span.andes-money-amount__fraction::text').getall()
                price_cents = shoes_content.css('span.andes-money-amount__cents::text').getall()
                
                yield {
                    "brand": shoes_content.css('span.poly-component__brand::text').get(),
                    "name": shoes_content.css('a::text').get(),
                    "old_price_reais": prices[0] if len(prices) >= 2 else None,
                    "old_price_cents": price_cents[0] if len(price_cents) >= 2 else None,
                    "new_price_reais": prices[1] if len(prices) >= 2 else None,
                    "new_price_cents": price_cents[1] if len(price_cents) >= 2 else None,
                    "reviews_rating_number": shoes_content.css('span.poly-reviews__rating::text').get(),
                    "reviews_amount": shoes_content.css('span.poly-reviews__total::text').get(),
                    "datetime": datetime.now().timestamp()
                }
                
        ### OBS: If the price list is of length = 1, the 'old_price_reais' will take the 'new_price_reais' value,
        # so this need to be validated on the silver layer
        
        yield scrapy.Request(
                url=response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get(),
                callback=self.parse
        )
