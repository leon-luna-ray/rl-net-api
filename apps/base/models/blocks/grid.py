from wagtail.blocks import (
    CharBlock,
    StreamBlock,
    StructBlock,
)
from apps.base.serializers import ApiImageChooserBlock

class LargeImageGridBlock(StructBlock):
    title = CharBlock()
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])

class SmallImageGridBlock(StructBlock):
    title = CharBlock()
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])

class FilmstripImagesBlock(StructBlock):
    title = CharBlock()
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])
