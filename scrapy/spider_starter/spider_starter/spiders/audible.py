from typing import Iterable
import scrapy


class AudibleSpider(scrapy.Spider): # basic spider template
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

    def start_requests(self):
        scrapy.Request(url=self.start_urls[0], callback=self.parse, headers={"User-Agent": f"{self.user_agent}"})
        return super().start_requests()

    def parse(self, response):

        product_container = response.xpath("//div[@class='adbl-impression-container ']/div/span/ul/li")

        for product in product_container:

            book_title = product.xpath(".//h3[contains(@class, 'bc-heading')]/a/text()").get()
            book_author = product.xpath(".//li[contains(@class, 'authorLabel')]/span/a/text()").getall()
            book_runtime = product.xpath(".//li[contains(@class, 'runtimeLabel')]/span/text()").getall()

            yield {
                "title": book_title,
                "author": book_author,
                "runtime": book_runtime,
                # "User-Agent": f"{self.user_agent}"
            }

        pagination = response.xpath("//ul[contains(@class,'pagingElements')]")
        next_page = pagination.xpath(".//span[contains(@class, 'nextButton')]/a/@href").get()

        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers={"User-Agent": f"{self.user_agent}"})

