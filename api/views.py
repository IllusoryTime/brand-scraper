from urllib.parse import urlparse

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


class ImageMetadataListAPIView(generics.ListAPIView):
    queryset = ImageMetadata.objects.all()
    serializer_class = ImageMetadataSerializer


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
