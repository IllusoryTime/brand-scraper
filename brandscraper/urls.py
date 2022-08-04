from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape_image/', views.ImageScrapperAPIView.as_view()),
    path('image/metadata/all', views.ImageMetadataListAPIView.as_view()),
    path('image/metadata/id/<uuid:pk>', views.ImageMetadataByIDRetrieveAPIView.as_view()),
    path('image/metadata/url/<str:web_page>', views.ImageMetadataByURLRetrieveAPIView.as_view()),
]
