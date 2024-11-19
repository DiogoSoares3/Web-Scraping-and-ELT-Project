import scrapy
from datetime import datetime

class MagaluTenisCorridaMasculinoSpider(scrapy.Spider):
    name = "magalu_tenis_corrida_masculino"
    allowed_domains = ["www.magazinevoce.com.br"]
    start_urls = ["https://www.magazinevoce.com.br/magazinevendasitemagalu/busca/tenis+corrida+masculino/"]

    def __init__(self):
        self.page = 1
        self.visited_pages = set()

    def parse(self, response):
        products = response.css('div.sc-gQSkpc.jTodsw')

        for product in products:

            yield {
                'name': product.css('h2.sc-cvalOF.cQhIqz::text').get(),
                'old_price': product.css('p.sc-dcJsrY.lmAmKF.sc-fyVfxW.egCHto::text').get(),
                'new_price': product.css('p.sc-dcJsrY.eLxcFM.sc-jdkBTo.etFOes::text').get(),
                'rating_and_number_of_evaluations': product.css('span.sc-fUkmAC.geJyjP::text').get(),
                'discount_pix': products.css('span.sc-bddgXz.iYagWw::text').getall()[1],
                'datetime': datetime.now().timestamp()
                }

        if products:
            next_page_url = f"https://www.magazinevoce.com.br/magazinevendasitemagalu/busca/tenis+corrida+masculino/?page={self.page + 1}"

            if self.page + 1 not in self.visited_pages:
                self.visited_pages.add(self.page + 1)
                yield scrapy.Request(url=next_page_url, callback=self.parse)

            self.page += 1
