from wagtail.blocks import (
    CharBlock,
    StreamBlock,
    StructBlock,
    ChoiceBlock,
)
from apps.base.serializers import ApiImageChooserBlock

# todo rm
class LargeImageGridBlock(StructBlock):
    title = CharBlock()
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])
# todo rm
class SmallImageGridBlock(StructBlock):
    title = CharBlock()
    images = StreamBlock([
        # Todo add choice to select collection as well.
        ('image', ApiImageChooserBlock())
    ])

class ImageGridBlock(StructBlock):
    grid_sizes = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    title = CharBlock()
    grid_size = ChoiceBlock(choices=grid_sizes, default='large')
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])

class FilmstripImagesBlock(StructBlock):
    title = CharBlock()
    images = StreamBlock([
        ('image', ApiImageChooserBlock())
    ])
