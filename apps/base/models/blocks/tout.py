from wagtail.blocks import (
    CharBlock,
    StreamBlock,
    StructBlock,
    ChoiceBlock,
)
from apps.base.serializers import ApiImageChooserBlock


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
