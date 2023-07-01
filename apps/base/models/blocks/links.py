from wagtail.blocks import (
    StreamBlock,
    StructBlock,
    URLBlock,
)

from apps.base.serializers.pages import ApiPageChooserBlock


class LinkBlock(StructBlock):
    link = StreamBlock(
        [
            ('page', ApiPageChooserBlock(
                required=False,
                icon='home',
            )),
            ('url', URLBlock(
                required=False,
                icon='link',
            )),
        ],
        max_num=1,
        required=True,
    )
