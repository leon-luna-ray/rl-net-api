from django.db import models

from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models.collections import Collection
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from apps.base.models.pages import BasePage
from apps.base.serializers.images import CollectionSerializer, ApiImageChooserBlock
from apps.base.models.blocks.content import PageContentBlock

GRID_SIZES = [
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large'),
]


class CollectionsLandingPage(BasePage):
    """Page model for saving gallery collection pages"""
    max_count = 1
    subpage_types = ['gallery.CollectionDetailPage']


class CollectionDetailPage(BasePage):
    """Page model for collection detail page"""

    hero_images = StreamField(
        [
            ('image', ApiImageChooserBlock(required=True)),
        ],
        min_num=1,
        null=True,
        blank=False,
        use_json_field=True,
    )

    intro = RichTextField(
        null=True,
        blank=True,
    )

    page_content = StreamField(
        PageContentBlock(),
        null=True,
        use_json_field=True,
    )

    content_panels = BasePage.content_panels + [
        FieldPanel('hero_images'),
        FieldPanel('intro'),
        FieldPanel('page_content'),
    ]
    api_fields = [
        APIField('hero_images'),
        APIField('intro'),
        APIField('page_content'),
    ]

    subpage_types = []

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

    hero_images = StreamField(
        [
            ('image', ApiImageChooserBlock(required=True)),
        ],
        min_num=1,
        null=True,
        blank=False,
        use_json_field=True,
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
        max_length=10,
        choices=GRID_SIZES,
        default='large'
    )

    page_content = StreamField(
        PageContentBlock(),
        null=True,
        use_json_field=True,
    )

    content_panels = BasePage.content_panels + [
        FieldPanel('is_public'),
        FieldPanel('hero_images'),
        FieldPanel('intro'),
        FieldPanel('location'),
        FieldPanel('image_collection'),
        FieldPanel('grid_size'),
        FieldPanel('page_content'),
    ]
    api_fields = [
        APIField('is_public'),
        APIField('hero_images'),
        APIField('intro'),
        APIField('location'),
        APIField('image_collection', serializer=CollectionSerializer()),
        APIField('grid_size'),
        APIField('page_content'),
    ]

    subpage_types = []
