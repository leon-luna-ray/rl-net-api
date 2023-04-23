from django.conf import settings
from rest_framework import serializers
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock

from apps.base.models.images import AccessibleImage

MEDIA_URL = '' if settings.S3_ENABLED else settings.WAGTAILADMIN_BASE_URL


class ImageSerializer(serializers.ModelSerializer):
    alt_text = serializers.SerializerMethodField('get_alt_text')
    caption = serializers.SerializerMethodField('get_caption')
    exif_data = serializers.SerializerMethodField('get_exif')
    large = serializers.SerializerMethodField('get_large_rendition')
    medium = serializers.SerializerMethodField('get_medium_rendition')
    original = serializers.SerializerMethodField('get_original_image')
    thumbnail = serializers.SerializerMethodField('get_thumbnail_rendition')


    def get_alt_text(self, obj):
        try:
            return obj.alt_text
        except Exception:
            return ''

    def get_caption(self, obj):
        try:
            return obj.caption
        except Exception:
            return ''

    def get_exif(self, obj):
        try:
            return obj.exif_data
        except Exception:
            return ''

    def get_original_image(self, obj):
        try:
            return f'{MEDIA_URL}{obj.file.url}'
        except Exception:
            return ''

    def get_medium_rendition(self, obj):
        try:
            rendition = f'{MEDIA_URL}{obj.get_rendition("width-800").url}'

            return rendition
        except Exception:
            return ''

    def get_large_rendition(self, obj):
        try:
            rendition = f'{MEDIA_URL}{obj.get_rendition("width-1200").url}'

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
            'filename',
            'file_size',
            "focal_point_x",
            "focal_point_y",
            "focal_point_width",
            "focal_point_height",
            'id',
            'large',
            'medium',
            'original',
            'thumbnail',
        )


class ApiImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value and value is not None:
            return ImageSerializer(value, context=context).to_representation(value)
