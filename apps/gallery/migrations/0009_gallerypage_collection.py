# Generated by Django 4.1.8 on 2023-04-24 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('gallery', '0008_rename_gallerylandingpage_collectionslandingpage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallerypage',
            name='collection',
            field=models.ManyToManyField(to='wagtailcore.collection'),
        ),
    ]
