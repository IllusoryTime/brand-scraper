import uuid

from django.db import models


class WebPage(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, verbose_name='ID')
    url = models.URLField(unique=True)


class ImageMetadata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    web_page = models.ForeignKey(
        to=WebPage, on_delete=models.SET_NULL, null=True)
    image_url = models.URLField()
    file_name = models.CharField(max_length=255)
    height = models.FloatField()
    width = models.FloatField()
    scrape_date = models.DateField()
    file_size = models.FloatField()
