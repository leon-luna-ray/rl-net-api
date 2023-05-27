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
    large = serializers.SerializerMethodField('get_large_rendition')
    medium = serializers.SerializerMethodField('get_medium_rendition')
    original = serializers.SerializerMethodField('get_original_image')
    thumbnail = serializers.SerializerMethodField('get_thumbnail_rendition')
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, slug_field='name')


    def get_original_image(self, obj):
        try:
            return f'{MEDIA_URL}{obj.file.url}'
        except Exception:
            return ''

    def get_medium_rendition(self, obj):
        try:
            rendition = f'{MEDIA_URL}{obj.get_rendition("width-600").url}'

            return rendition
        except Exception:
            return ''

    def get_large_rendition(self, obj):
        try:
            rendition = f'{MEDIA_URL}{obj.get_rendition("width-1000").url}'

            return rendition
        except Exception:
            return ''

    def get_thumbnail_rendition(self, obj):
        try:
            rendition = f'{MEDIA_URL}{obj.get_rendition("fill-400x400").url}'

            return rendition
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
            # "focal_point_x",
            # "focal_point_y",
            # "focal_point_width",
            # "focal_point_height",
            'id',
            'large',
            'medium',
            'original',
            'thumbnail',
            'tags',
        )


class ApiImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value and value is not None:
            return ImageSerializer(value, context=context).to_representation(value)


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

