from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField

from .models import AlbumDetailPage

class AlbumDetailPageSerializer(serializers.ModelSerializer):
    first_five_images = serializers.SerializerMethodField()

    class Meta:
        model = AlbumDetailPage
        fields = ['title', 'intro', 'preview_images']

    def get_preview_images(self, obj):
        images = obj.image_collection.get_images()
        rendition_field = ImageRenditionField('fill-400x400')
        return [rendition_field(image) for image in images[:5]]
