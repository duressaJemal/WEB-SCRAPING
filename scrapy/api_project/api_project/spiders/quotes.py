import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        json_response = json.loads(response.body)
        quotes = json_response["quotes"]

        for qoute in quotes:

            yield {
                "author": qoute.get("author").get("name"),
                "quote": qoute.get("text"),
                "tags": qoute.get("tags")
            }

        has_next = json_response["has_next"]
        if has_next:
            next_page = json_response["page"] + 1
            yield scrapy.Request(
                url=f"https://quotes.toscrape.com/api/quotes?page={next_page}",
                callback=self.parse
            )

