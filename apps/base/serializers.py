from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import Field
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import PageChooserBlock

MEDIA_URL = '' if settings.S3_ENABLED else settings.WAGTAILADMIN_BASE_URL

# Serializers


class ImageSerializer(serializers.ModelSerializer):
    alt_text = serializers.SerializerMethodField('get_alt_text')
    caption = serializers.SerializerMethodField('get_caption')
    original = serializers.SerializerMethodField('get_original')
    medium = serializers.SerializerMethodField('get_medium')
    thumbnail = serializers.SerializerMethodField('get_thumbnail')

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

    def get_original(self, obj):
        try:
            return f'{MEDIA_URL}{obj.file.url}'
        except Exception:
            return ''

    def get_medium(self, obj):
        try:
            rendition = f'{MEDIA_URL}{obj.get_rendition("width-800").url}'

            return rendition
        except Exception:
            return ''

    def get_thumbnail(self, obj):
        try:
            rendition = f'{MEDIA_URL}{obj.get_rendition("fill-400x400").url}'

            return rendition
        except Exception:
            return ''

    class Meta:
        model = Image
        fields = (
            'title',
            'alt_text',
            'caption',
            "collection",
            'file',
            'filename',
            'file_size',
            "focal_point_x",
            "focal_point_y",
            "focal_point_width",
            "focal_point_height",
            'height',
            'id',
            'medium',
            'original',
            # "tags",
            'thumbnail',
            'width',
        )


def _serializePage(value):
    return {
        "title": value.title,
        "id": value.id,
        "slug": value.slug,
        "path": value.get_url(),
    }


# Fields


class PageSerializerField(Field):
    def to_representation(self, value):
        if value:
            return _serializePage(value)
# Blocks


class ApiImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value and value is not None:
            return ImageSerializer(value, context=context).to_representation(value)


class ApiPageChooserBlock(PageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return _serializePage(value)
