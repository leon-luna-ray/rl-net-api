# Generated by Django 4.1.7 on 2023-02-27 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_gallerypage_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallerypage',
            name='images',
        ),
    ]