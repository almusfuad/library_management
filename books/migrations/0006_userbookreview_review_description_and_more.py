# Generated by Django 5.0 on 2024-01-04 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_book_average_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbookreview',
            name='review_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userbookreview',
            name='user_review',
            field=models.CharField(choices=[('5', 'Excellent'), ('4', 'Good'), ('3', 'Average'), ('2', 'Fair'), ('1', 'Poor')], max_length=5),
        ),
    ]
