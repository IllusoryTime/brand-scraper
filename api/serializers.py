from rest_framework import serializers

from api.models import WebPage, ImageMetadata


class WebPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebPage
        fields = ["id", "url"]


class ImageMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMetadata
        fields = [
            "id",
            "web_page",
            "image_url",
            "file_name",
            "height",
            "width",
            "scrape_date",
            "file_size"
        ]
