# Generated by Django 5.0 on 2024-01-04 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_userbookreview_review_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
