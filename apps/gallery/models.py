from django.db import models

from wagtail.api import APIField
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Collection
from wagtail.admin.panels import FieldPanel

from apps.base.serializers import ApiImageChooserBlock
from apps.base.models.pages import BasePage

COLLECTION_CHOICES = ((c.id, c.name) for c in Collection.objects.all())

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
    collection = models.ForeignKey(
        'wagtailcore.Collection',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
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
        APIField('collection'),
    ]

    subpage_types = []