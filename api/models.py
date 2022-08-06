import uuid

from django.db import models


class WebPage(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField(unique=True)


class ImageMetadata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    web_page = models.ForeignKey(to=WebPage, on_delete=models.SET_NULL, null=True)
    file_name = models.CharField(max_length=255)
    height = models.IntegerField()
    width = models.IntegerField()
    scrape_date = models.DateField()
    file_size = models.DecimalField(max_digits=8, decimal_places=2)
    mode = models.CharField(max_length=32)
    format = models.CharField(max_length=32)
