from wagtail.blocks import (
    CharBlock,
    StreamBlock,
    StructBlock,
)
from apps.base.serializers import ApiImageChooserBlock


class FeaturedImagesBlock(StructBlock):
    title = CharBlock()
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])
