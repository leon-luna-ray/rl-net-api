from django.db import models
from wagtail.images.models import Image, AbstractImage, AbstractRendition


class AccessibleImage(AbstractImage):
    """
    Adds extra fields to wagtail image model.
    """
    alt_text = models.TextField(blank=True)
    caption = models.TextField(blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'alt_text',
        'caption',
    )


class AccessibleRendition(AbstractRendition):
    """
    AccessibleRendition Model
    Stores renditions for the custom model.
    """

    image = models.ForeignKey(
        AccessibleImage,
        on_delete=models.CASCADE,
        related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
