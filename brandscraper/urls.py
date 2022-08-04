from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape_image/', views.ImageScrapperAPIView.as_view()),
    path('image/metadata/id/<uuid:pk>', views.ImageMetadataDetailByIDAPIView.as_view()),
    path('image/metadata/url/<str:web_page>', views.ImageMetadataDetailByURLAPIView.as_view()),
]
