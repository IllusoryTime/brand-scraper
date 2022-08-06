from rest_framework import serializers

from api.models import WebPage, ImageMetadata


class WebPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebPage
        fields = "__all__"
        extra_kwargs = {
            'url': {'validators': []}
        }


class ImageMetadataSerializer(serializers.ModelSerializer):
    web_page = serializers.CharField(source='web_page.url')

    class Meta:
        model = ImageMetadata
        fields = "__all__"
        extra_kwargs = {
            'file_size': {'coerce_to_string': False}
        }
