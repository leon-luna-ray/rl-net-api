# Generated by Django 4.1.7 on 2023-02-27 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_gallerypage_collections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallerypage',
            name='collections',
        ),
    ]