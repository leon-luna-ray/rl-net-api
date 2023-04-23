from django.db import models

from wagtail.api import APIField
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel

from apps.base.serializers import ImageSerializer
from apps.base.models.pages import BasePage
from apps.base.models.blocks.content import HomePageContentBlock

class HomePage(BasePage):
    subtitle = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    text = models.CharField(max_length=255, null=True)

    intro = RichTextField(
        null=True,
        blank=True,
    )
    hero_image = models.ForeignKey(
        'base.AccessibleImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    page_content = StreamField(
        HomePageContentBlock(),
        null=True,
        use_json_field=True,
    )

    content_panels = BasePage.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('intro'),
        FieldPanel('hero_image'),
        FieldPanel('page_content'),
        FieldPanel('text'),
    ]
    api_fields = [
        APIField('subtitle'),
        APIField('intro'),
        APIField('hero_image', serializer=ImageSerializer()),
        APIField('page_content'),
        APIField('text'),
    ]

    max_count = 1
    subpage_types = ['gallery.CollectionsLandingPage']
