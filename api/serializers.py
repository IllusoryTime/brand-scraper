from django.templatetags.static import static
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
    image_url = serializers.SerializerMethodField()  # TODO: Come back to here

    class Meta:
        model = ImageMetadata
        fields = "__all__"
        extra_kwargs = {
            'file_size': {'coerce_to_string': False}
        }

    @staticmethod
    def get_image_url(obj):
        return static(obj.file_name)
