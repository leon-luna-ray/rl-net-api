# Generated by Django 4.1.8 on 2023-06-08 04:45

import apps.base.serializers.images
from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_remove_homepage_hero_image_homepage_hero_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='hero_images',
            field=wagtail.fields.StreamField([('hero_image', wagtail.blocks.StructBlock([('image', apps.base.serializers.images.ApiImageChooserBlock()), ('text', wagtail.blocks.CharBlock(required=False)), ('text_color', wagtail.blocks.ChoiceBlock(choices=[('black', 'Black'), ('white', 'White')])), ('text_position', wagtail.blocks.ChoiceBlock(choices=[('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom')]))], required=False))], blank=True, null=True, use_json_field=True),
        ),
    ]
