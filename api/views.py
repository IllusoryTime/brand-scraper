import base64
import os
from io import BytesIO
from urllib.parse import urlparse

from PIL import Image
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from scrapyd_api import ScrapydAPI
from url_normalize import url_normalize

from api.models import ImageMetadata
from api.serializers import WebPageSerializer, ImageMetadataSerializer
from api.utils import is_valid_uuid

scrapyd = ScrapydAPI('http://localhost:6800')


class ImageScrapperAPIView(generics.CreateAPIView):
    serializer_class = WebPageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            url = url_normalize(serializer.validated_data['url'])
            domain = urlparse(url).netloc
            task = scrapyd.schedule('default', 'image', url=url, domain=domain)

            return Response({'task_id': task, 'status': 'started'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImageMetadata.objects.all()

    def list(self, request, *args, **kwargs):
        url = request.GET.get('url', None)
        size = request.GET.get('size', None)

        if url:
            normalized_url = url_normalize(url)
            file_names = ImageMetadata.objects \
                .filter(web_page__url__iexact=normalized_url) \
                .values_list('file_name', flat=True)

            try:
                image_data = [self.get_image_data(file_name, size) for file_name in file_names]
                return Response(image_data, status=status.HTTP_200_OK)
            except():
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        size = request.GET.get('size', None)

        if not is_valid_uuid(pk):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        image_metadata = get_object_or_404(ImageMetadata, pk=pk)

        try:
            image_data = self.get_image_data(image_metadata.file_name, size)
            return Response(image_data, status=status.HTTP_200_OK)
        except():
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_image_data(file_name, size=None):
        image_path = os.path.abspath(os.getcwd()) + static(file_name)
        image = Image.open(image_path)

        if size:
            size_dict = {"small": 256, "medium": 1024, "large": 2048}
            width = size_dict.get(size.lower(), None)

            if width:
                image.thumbnail((size, image.height), Image.ANTIALIAS)

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_data = base64.b64encode(buffered.getvalue())

        return image_data


class ImageMetadataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImageMetadata.objects.all()

    def list(self, request, *args, **kwargs):
        """
        If no url query parameter is passed we are sending all the records.
        Because in standard GET API data should always be sent. Query parameters are used for filtering.
        """

        queryset = self.queryset
        url = request.GET.get('url', None)

        if url:
            normalized_url = url_normalize(url)
            queryset = ImageMetadata.objects.filter(web_page__url__iexact=normalized_url)

        serializer = ImageMetadataSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        if not is_valid_uuid(pk):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        image_metadata = get_object_or_404(ImageMetadata, pk=pk)
        serializer = ImageMetadataSerializer(image_metadata)
        return Response(serializer.data)
