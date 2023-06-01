from django.conf import settings

from rest_framework import serializers
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models.collections import Collection
from taggit.models import Tag
from apps.base.models.images import AccessibleImage

MEDIA_URL = '' if settings.S3_ENABLED else settings.WAGTAILADMIN_BASE_URL


class ImageSerializer(serializers.ModelSerializer):
    alt_text = serializers.CharField(default='')
    caption = serializers.CharField(default='')
    exif_data = serializers.CharField(default='')
    original = serializers.SerializerMethodField('get_original_image')
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(), many=True, slug_field='name')
    renditions = serializers.SerializerMethodField()

    def get_renditions(self, obj):
        rendition_sizes = {
            "large": "max-1080x1080",
            "medium": "max-600x600",
            "thumbnail": "fill-400x400"
        }

        renditions = {}

        for key, filter_spec in rendition_sizes.items():
            rendition = obj.get_rendition(filter_spec)
            if rendition:
                rendition_url = f"{MEDIA_URL}{rendition.url}"
                renditions[key] = rendition_url

        return renditions

    def get_original_image(self, obj):
        try:
            return f'{MEDIA_URL}{obj.file.url}'
        except Exception:
            return ''

    class Meta:
        model = AccessibleImage
        fields = (
            'title',
            'alt_text',
            'caption',
            "collection",
            "exif_data",
            'id',
            'original',
            'tags',
            'renditions',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class ApiImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value and value is not None:
            serializer = ImageSerializer(value, context=context)
            representation = serializer.to_representation(value)
            representation['exif_data'] = value.exif_data
            representation['caption'] = value.caption
            representation['alt_text'] = value.alt_text
            representation['tags'] = [tag.name for tag in value.tags.all()]
            return representation
        return None




class CollectionSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = AccessibleImage.objects.filter(collection=obj)
        return ImageSerializer(images, many=True, context=self.context).data

    class Meta:
        model = Collection
        fields = ['id', 'name', 'images']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = representation.pop('images', [])
        return representation
