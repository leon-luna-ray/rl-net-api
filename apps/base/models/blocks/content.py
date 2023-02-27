from wagtail.blocks import (
    StreamBlock,
)
from apps.base.models.blocks.grid import FeaturedImagesBlock

class HomePageContentBlock(StreamBlock):
    featured_images = FeaturedImagesBlock()