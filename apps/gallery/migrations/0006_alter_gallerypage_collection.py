# Generated by Django 4.1.7 on 2023-02-27 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('gallery', '0005_remove_gallerypage_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallerypage',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.collection'),
        ),
    ]