from django.conf import settings
from rest_framework.fields import Field

from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import PageChooserBlock

MEDIA_URL = '' if settings.S3_ENABLED else settings.WAGTAILADMIN_BASE_URL

# Serializers


def _serializeImage(value):
    return {
        "title": value.title,
        "alt_text": value.alt_text,
        "caption": value.caption,
        "id": value.id,
        "medium": f'{MEDIA_URL}{value.get_rendition("width-800").url}',
        "original": f'{MEDIA_URL}{value.file.url}',
        "thumbnail": f'{MEDIA_URL}{value.get_rendition("fill-400x400").url}',
    }


def _serializePage(value):
    return {
        "title": value.title,
        "id": value.id,
        "slug": value.slug,
        "path": value.get_url(),
    }


# Fields


class ImageSerializerField(Field):
    def to_representation(self, value):
        if value:
            return _serializeImage(value)


class PageSerializerField(Field):
    def to_representation(self, value):
        if value:
            return _serializePage(value)
# Blocks


class ApiImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return _serializeImage(value)


class ApiPageChooserBlock(PageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return _serializePage(value)
