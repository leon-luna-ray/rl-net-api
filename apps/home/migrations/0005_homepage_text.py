# Generated by Django 4.1.8 on 2023-04-23 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_homepage_page_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='text',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
