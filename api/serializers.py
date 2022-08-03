from django.templatetags.static import static
from rest_framework import serializers

from api.models import WebPage, ImageMetadata


class WebPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebPage
        fields = "__all__"


class ImageMetadataSerializer(serializers.ModelSerializer):
    web_page = serializers.CharField(source='web_page.url')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageMetadata
        fields = "__all__"

    def get_image_url(self, obj):
        return static(obj.file_name)
