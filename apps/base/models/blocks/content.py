from wagtail.blocks import (
    StreamBlock,
)
from apps.base.models.blocks.tout import CallToActionBlock
from apps.base.models.blocks.grid import (
    FilmstripImagesBlock,
    ImageGridBlock,
    )

class PageContentBlock(StreamBlock):
    call_to_action = CallToActionBlock()
    filmstrip_images = FilmstripImagesBlock()
    image_grid = ImageGridBlock()

