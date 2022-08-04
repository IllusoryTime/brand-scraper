import scrapy


class ImageSpider(scrapy.Spider):
    name = 'image'

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.start_urls = [kwargs.get('url')]
        self.allowed_domains = [kwargs.get('domain')]

    def parse(self, response, **kwargs):
        """
        We are parsing img, .image and ::attr(src).
        """
        
        raw_image_urls = response.css('.image img ::attr(src)').getall()
        clean_image_urls = [response.urljoin(img_url) for img_url in raw_image_urls]

        yield {
            'image_urls': clean_image_urls
        }
