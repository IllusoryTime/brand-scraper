from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image_metadata/id/<uuid:pk>', views.ImageMetadataDetailByIDAPIView.as_view()),
    path('image_metadata/url/<str:web_page>', views.ImageMetadataDetailByURLAPIView.as_view()),
]
