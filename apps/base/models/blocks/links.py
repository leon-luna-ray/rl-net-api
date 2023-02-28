from wagtail.core.blocks import (
    CharBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)

from .api import ApiPageChooserBlock


class LinkWithTitleBlock(StructBlock):
    title = CharBlock()
    link = StreamBlock(
        [
            ('page_link', ApiPageChooserBlock(
                required=False,
                icon='home',
            )),
            ('external_link', URLBlock(
                required=False,
                icon='link',
            )),
        ],
        max_num=1,
        required=True,
    )
