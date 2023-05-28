from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import serializers
from wagtail.images.views.serve import generate_signature
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models.collections import Collection
from taggit.models import Tag
from apps.base.models.images import AccessibleImage, AccessibleRendition

MEDIA_URL = '' if settings.S3_ENABLED else settings.WAGTAILADMIN_BASE_URL

@receiver(post_save, sender=AccessibleImage)
def create_renditions(sender, instance, created, **kwargs):
    if created:
        instance.create_renditions()

class ImageSerializer(serializers.ModelSerializer):
    alt_text = serializers.CharField(default='')
    caption = serializers.CharField(default='')
    exif_data = serializers.CharField(default='')
    original = serializers.SerializerMethodField('get_original_image')
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(), many=True, slug_field='name')
    renditions = serializers.SerializerMethodField()

    def get_renditions(self, obj):
        renditions = {}
        for filter_spec in ['max-1200x1200', 'max-800x800', 'fill-400x400']:
            rendition = obj.get_rendition(filter_spec)
            if rendition:
                rendition_url = rendition.url
                rendition_signature = generate_signature(rendition_url, filter_spec)
                renditions[filter_spec] = {
                    'url': rendition_url,
                    'signature': rendition_signature
                }
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
