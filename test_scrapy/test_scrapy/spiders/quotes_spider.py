import scrapy

class QuotesSpider(scrapy.Spider):
    name = "desk"

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
    }

    def __init__(self, urls=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(',') if urls else []

    def start_requests(self):
        if not self.start_urls:
            self.start_urls = [
                "https://www.amazon.com/dp/B08LZ4D3R2"  # Example URL
            ]

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                },
                callback=self.parse
            )

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to fetch the page: {response.url} with status code {response.status}.")
            return

        # Check and log the response for debugging
        self.logger.info(f"Response URL: {response.url}")

        # Attempt to extract the title and image URL
        title = response.css('h1 span#productTitle::text').get()
        if title:
            title = title.strip()
        else:
            title = "Title not found"

        image_url = response.css('img#landingImage::attr(src)').get()
        if not image_url:
            image_url = "Image URL not found"

        # Log the extracted information for debugging
        self.logger.info(f"Scraped: {title} - {image_url}")

        yield {
            "title": title,
            "image_url": image_url,
            "product_url": response.url
        }
