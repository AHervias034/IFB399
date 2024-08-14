from pathlib import Path
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "desk"
    allowed_domains = ["ceofficeconcepts.com.au"]
    start_urls = ["https://www.ceofficeconcepts.com.au/desks"]

    def start_requests(self):
        urls = [
            "https://www.ceofficeconcepts.com.au/desks"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for items in response.css('div.span4'):
            yield{
                "text": items.css("h2.product-title a::attr(title)").get(),
                "link": items.css("h2.product-title a::attr(href)").get(),
            }
