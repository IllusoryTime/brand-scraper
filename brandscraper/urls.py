from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape_image/', views.ImageScrapperAPIView.as_view()),
    path('image/metadata/', views.ImageMetadataViewSet.as_view({'get': 'list'})),
    path('image/metadata/<str:pk>', views.ImageMetadataViewSet.as_view({'get': 'retrieve'})),
]
