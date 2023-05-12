# Generated by Django 4.1.8 on 2023-05-12 05:13

import apps.base.serializers.images
from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_homepage_page_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='text',
        ),
        migrations.AlterField(
            model_name='homepage',
            name='page_content',
            field=wagtail.fields.StreamField([('filmstrip_images', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('images', wagtail.blocks.StreamBlock([('image', apps.base.serializers.images.ApiImageChooserBlock())]))])), ('large_image_grid', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('images', wagtail.blocks.StreamBlock([('image', apps.base.serializers.images.ApiImageChooserBlock())]))])), ('small_image_grid', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('images', wagtail.blocks.StreamBlock([('image', apps.base.serializers.images.ApiImageChooserBlock())]))]))], null=True, use_json_field=True),
        ),
    ]
