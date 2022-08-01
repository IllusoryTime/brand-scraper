from django.contrib import admin

from api.models import ImageMetadata, WebPage


class WebPageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WebPage._meta.fields]


class ImageMetadataAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ImageMetadata._meta.fields]


admin.site.register(WebPage, WebPageAdmin)
admin.site.register(ImageMetadata, ImageMetadataAdmin)
