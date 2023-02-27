from django.db import models

from wagtail.api import APIField
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel

from apps.base.serializers import ApiImageChooserBlock
from apps.base.models.pages import BasePage


class GalleryLandingPage(BasePage):
    """Page model for saving gallery pages"""
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
    # TODO replace with gallery collection block
    images = StreamField([
        ('image', ApiImageChooserBlock()),
    ])

    content_panels = BasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('location'),
        FieldPanel('images'),

    ]
    api_fields = [
        APIField('intro'),
        APIField('location'),
        APIField('images'),
    ]

    subpage_types = []