from django.db import models

from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models.collections import Collection
from wagtail.admin.panels import FieldPanel

from apps.base.models.pages import BasePage
from apps.base.serializers.images import CollectionSerializer


class CollectionsLandingPage(BasePage):
    """Page model for saving gallery collection pages"""
    max_count = 1
    subpage_types = ['gallery.GalleryPage']


class GalleryPage(BasePage):
    """Page model for image gallery page"""
    intro = RichTextField(
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name='+',
    )

    content_panels = BasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('location'),
        FieldPanel('collection'),
    ]
    api_fields = [
        APIField('intro'),
        APIField('location'),
        APIField('collection', serializer=CollectionSerializer()),
    ]

    subpage_types = []
