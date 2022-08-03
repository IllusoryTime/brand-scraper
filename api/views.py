from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, views

from api.models import ImageMetadata
from api.serializers import ImageMetadataSerializer


class ImageMetadataDetailByIDAPIView(generics.RetrieveAPIView):
    queryset = ImageMetadata.objects.all()
    serializer_class = ImageMetadataSerializer


class ImageMetadataDetailByURLAPIView(generics.RetrieveAPIView):
    serializer_class = ImageMetadataSerializer

    def get_object(self):
        return get_object_or_404(ImageMetadata, web_page__url__iexact=self.kwargs.get('web_page'))
