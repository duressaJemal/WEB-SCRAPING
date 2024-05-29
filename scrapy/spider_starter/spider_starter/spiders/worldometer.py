import scrapy


class WorldometerSpider(scrapy.Spider): # basic spider template
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = [
        "https://www.worldometers.info/world-population/population-by-country"
    ]

    def parse(self, response):

        title = response.xpath("//h1/text()").get() # /text() is used to get the text of the tag .get() and .getall() is used to get the text of the tag
        countries = response.xpath("//td/a")

        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # yield {
            #     "country_name": country_name,
            #     "link": link
            #     }

            # absolute_url = f"https://www.worldometers.info{link}"
            # absolute_url = response.urljoin(link) # This is used to join the relative url with the base url
            # yield scrapy.Request(url=absolute_url) # This is used to make a request to the absolute url

            # relative_url_request
            # yield response.follow(url=link) # This is used to make a request to the relative url

            yield response.follow(url=link, callback=self.parse_country, meta={"country": country_name})

    def parse_country(self, response):

        country_name = response.request.meta["country"]
        rows = response.xpath("(//table[contains(@class, 'table')])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {
                "country_name": country_name,
                "year": year,
                "population": population
            }


