from wagtail.blocks import (
    CharBlock,
    StructBlock,
    ChoiceBlock,
    TextBlock,
)
from apps.base.serializers import ApiImageChooserBlock
from apps.base.models.blocks.links import LinkBlock

class HeroImageBlock(StructBlock):
    text_colors = [
        ('black', 'Black'),
        ('white', 'White'),
    ]
    text_positions = [
        ('top', 'Top'),
        ('middle', 'Middle'),
        ('bottom', 'Bottom'),
    ]

    image = ApiImageChooserBlock()
    text = CharBlock(required=False)
    text_color = ChoiceBlock(choices=text_colors, default='white')
    text_position = ChoiceBlock(choices=text_positions, default='middle')

class CallToActionBlock(StructBlock):
    title = CharBlock()
    text = TextBlock(required=False)
    image = ApiImageChooserBlock()
    link = LinkBlock()