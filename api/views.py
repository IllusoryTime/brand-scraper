from urllib.parse import urlparse

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from scrapyd_api import ScrapydAPI
from url_normalize import url_normalize

from api.models import ImageMetadata
from api.serializers import WebPageSerializer, ImageMetadataSerializer

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


class ImageMetadataListAPIView(generics.ListAPIView):
    queryset = ImageMetadata.objects.all()
    serializer_class = ImageMetadataSerializer


class ImageMetadataByIDRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ImageMetadata.objects.all()
    serializer_class = ImageMetadataSerializer


class ImageMetadataByURLRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ImageMetadataSerializer

    def get_object(self):
        return get_object_or_404(ImageMetadata, web_page__url__iexact=self.kwargs.get('web_page'))
