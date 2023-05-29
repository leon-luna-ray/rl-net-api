from django.db import models

from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models.collections import Collection
from wagtail.admin.panels import FieldPanel

from apps.base.models.pages import BasePage
from apps.base.serializers.images import CollectionSerializer

GRID_SIZES = [
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large'),
]


class CollectionsLandingPage(BasePage):
    """Page model for saving gallery collection pages"""
    max_count = 1
    # subpage_types = ['gallery.GalleryPage']


class AlbumsLandingPage(BasePage):
    """Page model for saving gallery collection pages"""
    max_count = 1
    subpage_types = ['gallery.AlbumDetailPage']


class AlbumDetailPage(BasePage):
    """Page model for Album detail page"""

    is_public = models.BooleanField(
        default=False,
        help_text="Check this box if the album is public."
    )

    intro = RichTextField(
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    image_collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name='+',
    )

    grid_size = models.CharField(
        max_length=10, choices=GRID_SIZES, default='large')

    content_panels = BasePage.content_panels + [
        FieldPanel('is_public'),
        FieldPanel('intro'),
        FieldPanel('location'),
        FieldPanel('image_collection'),
        FieldPanel('grid_size'),
    ]
    api_fields = [
        APIField('is_public'),
        APIField('intro'),
        APIField('location'),
        APIField('image_collection', serializer=CollectionSerializer()),
        APIField('grid_size'),

    ]

    subpage_types = []
