from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class BasePage(Page):
    """
    Base model for building pages. Child models will inherit from abtract base model. Abstract model does not create db table.
    """

    # SEO
    preview_thumbnail = models.ForeignKey(
        'base.AccessibleImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')

    promote_panels = Page.promote_panels + [
        FieldPanel('preview_thumbnail'),
    ]

    class Meta:
        abstract = True

    def json_ld(self):
        json = {
            '@context': 'https://schema.org/',
            '@type': 'WebPage',
            'name': getattr(self, 'title'),
        }

        return json