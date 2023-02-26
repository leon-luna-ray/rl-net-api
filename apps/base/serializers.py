from django.conf import settings
from rest_framework.fields import Field

from wagtail.images.blocks import ImageChooserBlock
# from wagtail.blocks import PageChooserBlock

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


# def _serializeProject(value):
#     return {
#         "title": value.title,
#         "description": value.description,
#         "id": value.id,
#         "path": value.get_url(),
#         "original_image": f'{MEDIA_URL}{value.main_image.file.url}',
#         "medium_image": f'{MEDIA_URL}{value.main_image.get_rendition("width-800").url}',
#         "project_url": value.project_url,
#         "repository_url": value.repository_url,
#         "slug": value.slug,
#         "thumbnail": f'{MEDIA_URL}{value.main_image.get_rendition("fill-400x400").url}',
#     }

# Fields


class ImageSerializerField(Field):
    def to_representation(self, value):
        if value:
            return _serializeImage(value)

# Blocks


class ApiImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return _serializeImage(value)


# class ApiProjectChooserBlock(PageChooserBlock):
#     def get_api_representation(self, value, context=None):
#         if value:
#             return _serializeProject(value)
