import scrapy


class LightingSpiderSpider(scrapy.Spider):
    name = "lighting_spider"
    allowed_domains = ["https://divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        # Проходим по всем карточкам товаров на странице
        for product in response.css('div._Ud0k'):
            yield {
                'name': product.css('span.ui-Ld-ZU::text').get().strip(),
                'price': product.css('div.pY3d2 span::text').get().replace('\u2009', '').strip(),
                'link': response.urljoin(product.css('a::attr(href)').get()),
            }

        # Пагинация: переход на следующую страницу
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)