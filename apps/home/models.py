from django.db import models

from wagtail.api import APIField
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel

from apps.base.serializers import ImageSerializer
from apps.base.models.pages import BasePage
from apps.base.models.blocks.content import HomePageContentBlock
from apps.base.serializers.images import ApiImageChooserBlock

class HomePage(BasePage):
    subtitle = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    intro = RichTextField(
        null=True,
        blank=True,
    )
    hero_images = StreamField(
        [
            ('image', ApiImageChooserBlock(required=False)),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    page_content = StreamField(
        HomePageContentBlock(),
        null=True,
        use_json_field=True,
    )

    content_panels = BasePage.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('intro'),
        FieldPanel('hero_images'),
        FieldPanel('page_content'),
    ]
    api_fields = [
        APIField('subtitle'),
        APIField('intro'),
        APIField('hero_images'),
        APIField('page_content'),
    ]

    max_count = 1
    subpage_types = ['gallery.CollectionsLandingPage', 'gallery.AlbumsLandingPage']
