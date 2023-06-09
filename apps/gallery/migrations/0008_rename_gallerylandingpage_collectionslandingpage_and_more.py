# Generated by Django 4.1.7 on 2023-03-01 03:12

import apps.base.serializers.images
from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('wagtailcore', '0083_workflowcontenttype'),
        ('gallery', '0007_remove_gallerypage_collection_gallerypage_images'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GalleryLandingPage',
            new_name='CollectionsLandingPage',
        ),
        migrations.AlterField(
            model_name='gallerypage',
            name='images',
            field=wagtail.fields.StreamField([('image', apps.base.serializers.images.ApiImageChooserBlock())], null=True, use_json_field=True),
        ),
    ]
