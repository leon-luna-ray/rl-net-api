# Generated by Django 4.1.7 on 2023-02-27 20:15

import apps.base.serializers
from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_hero_image_homepage_intro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='page_content',
            field=wagtail.fields.StreamField([('featured_images', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('images', wagtail.blocks.StreamBlock([('image', apps.base.serializers.ApiImageChooserBlock())]))]))], null=True, use_json_field=True),
        ),
    ]
