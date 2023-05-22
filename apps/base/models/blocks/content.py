from wagtail.blocks import (
    StreamBlock,
)
from apps.base.models.blocks.grid import (
    FilmstripImagesBlock,
    ImageGridBlock,
    )

class HomePageContentBlock(StreamBlock):
    filmstrip_images = FilmstripImagesBlock()
    image_grid = ImageGridBlock()