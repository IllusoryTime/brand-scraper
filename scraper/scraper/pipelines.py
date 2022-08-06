import datetime
import os

from PIL import Image
from scrapy.pipelines.images import ImagesPipeline

from api.models import WebPage, ImageMetadata


class ScraperPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        """
        Here we are processing the images downloaded by Scrapy image pipeline.
        We extract image metadata and save it to database.
        """

        webpage, created = WebPage.objects.get_or_create(url=spider.start_urls[0])

        if not created:
            ImageMetadata.objects.filter(web_page=webpage).delete()  # TODO: delete file as well

        image_metadata_list = []
        image_paths = [x['path'] for x in item['images']]

        for image_path in image_paths:
            relative_path = os.path.join(self.store.basedir, image_path)

            if os.path.isfile(relative_path):
                image = Image.open(relative_path)

                image_metadata = ImageMetadata(
                    web_page=webpage,
                    file_name=image_path,
                    height=image.height,
                    width=image.width,
                    scrape_date=datetime.date.today(),
                    file_size=os.path.getsize(relative_path) / 1024.0,
                    mode=image.mode,
                    format=image.format
                )

                image_metadata_list.append(image_metadata)

        # Using `bulk_create` to improve database performance.
        ImageMetadata.objects.bulk_create(image_metadata_list)

        return item
