from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from api import views

urlpatterns = [
    path('', RedirectView.as_view(url='scrape_image/')),
    path('admin/', admin.site.urls),
    path('scrape_image/', views.ImageScraperViewSet.as_view({'post': 'create'})),
    path('image/', views.ImageViewSet.as_view({'get': 'list'})),
    path('image/<str:pk>', views.ImageViewSet.as_view({'get': 'retrieve'})),
    path('image/metadata/', views.ImageMetadataViewSet.as_view({'get': 'list'})),
    path('image/metadata/<str:pk>', views.ImageMetadataViewSet.as_view({'get': 'retrieve'})),
]
