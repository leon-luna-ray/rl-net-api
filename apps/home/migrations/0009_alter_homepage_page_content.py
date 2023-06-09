# Generated by Django 4.1.8 on 2023-05-22 03:11

import apps.base.serializers.images
from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_homepage_page_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='page_content',
            field=wagtail.fields.StreamField([('filmstrip_images', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('images', wagtail.blocks.StreamBlock([('image', apps.base.serializers.images.ApiImageChooserBlock())]))])), ('image_grid', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('grid_size', wagtail.blocks.ChoiceBlock(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')])), ('images', wagtail.blocks.StreamBlock([('image', apps.base.serializers.images.ApiImageChooserBlock())]))]))], null=True, use_json_field=True),
        ),
    ]
