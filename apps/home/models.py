from django.db import models

from wagtail.api import APIField
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel

from apps.base.serializers import ImageSerializerField
from apps.base.models.pages import BasePage
# from apps.base.models.blocks import PageContentBlock

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
    hero_image = models.ForeignKey(
        'base.AccessibleImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    # Todo add page content
    # page_content = StreamField(
    #     PageContentBlock(
    #         null=True,
    #         blank=False,
    #     ),
    #     null=True,
    #     use_json_field=True,
    # )

    content_panels = BasePage.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('intro'),
        FieldPanel('hero_image'),
        # FieldPanel('page_content'),
    ]
    api_fields = [
        APIField('subtitle'),
        APIField('intro'),
        APIField('hero_image', serializer=ImageSerializerField()),
        # APIField('page_content'),
    ]

    max_count = 1
