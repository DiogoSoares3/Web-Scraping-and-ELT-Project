import scrapy


class PumaSpider(scrapy.Spider):
    name = "puma"
    allowed_domains = ["br.puma.com"]
    start_urls = ["https://br.puma.com/homens/calcados.html"]

    def __init__(self):
        self.page = 1
        self.visited_pages = set()

    def parse(self, response):
        products = response.css('div.product-item')

        for product in products:
            ultimos_tamanhos = bool(product.css('.product-item__label-text.js-product-label-text'))
            yield {
                'name': product.css('a.product-item__name::text').get(default='').strip(),
                'price': product.css('span.price::text').get(default='').strip(),
                'label': product.css('div.product-item__label-text::text').get(default='').strip(),
                'ultimos_tamanhos': ultimos_tamanhos
            }

        if products:
            next_page_url = f"https://br.puma.com/homens/calcados.html?p={self.page + 1}"

            if self.page + 1 not in self.visited_pages:
                self.visited_pages.add(self.page + 1)
                yield scrapy.Request(url=next_page_url, callback=self.parse)

            self.page += 1
