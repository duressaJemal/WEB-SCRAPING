import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider): # crawl spider template
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies_letter-X"]

    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

    rules = (
        # alow: regular expression that the (absolute) urls must match
        # deny: regular expression that the (absolute) urls must not match
        # restrict_xpaths: list of XPaths which restricts the portion of the page to which the rule is applied

        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='scripts-list']/a")), callback="parse_item", follow=True, process_request="set_user_agent"),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@rel='next'])[1]")), process_request="set_user_agent") # This is used to go to the next page(pagination)

         )

    def start_requests(self): # This is used to set the user agent for the request
        scrapy.Request(url=self.start_urls[0], headers={"User-Agent": f"{self.user_agent}"})
        return super().start_requests()

    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):

        article = response.xpath("//article[@class='main-article']")

        yield {
            "title": article.xpath(".//h1/text()").get(),
            "description": article.xpath(".//p/text()").get(),
            # "transcript": article.xpath(".//div/text()").getall(), # too much data
            # "url": response.url,
            # "User-Agent": response.request.headers["User-Agent"]
        }
