# Generated by Django 5.0 on 2024-01-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_remove_userbookreview_review_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='average_reviews',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]