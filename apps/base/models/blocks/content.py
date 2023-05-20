from wagtail.blocks import (
    StreamBlock,
)
from apps.base.models.blocks.grid import (
    FilmstripImagesBlock,
    LargeImageGridBlock,
    SmallImageGridBlock,
    ImageGridBlock,
    )

class HomePageContentBlock(StreamBlock):
    filmstrip_images = FilmstripImagesBlock()
    large_image_grid = LargeImageGridBlock()
    small_image_grid = SmallImageGridBlock()
    image_grid = ImageGridBlock()