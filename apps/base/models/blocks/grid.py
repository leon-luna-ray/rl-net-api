from wagtail.blocks import (
    CharBlock,
    StreamBlock,
    StructBlock,
    ChoiceBlock,
)
from apps.base.serializers import ApiImageChooserBlock

class ImageGridBlock(StructBlock):
    grid_sizes = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    title = CharBlock(required=False)
    grid_size = ChoiceBlock(choices=grid_sizes, default='large')
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])

class FilmstripImagesBlock(StructBlock):
    title = CharBlock()
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])
