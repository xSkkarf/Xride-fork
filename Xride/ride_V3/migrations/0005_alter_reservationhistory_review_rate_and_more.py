# Generated by Django 5.1.1 on 2025-01-27 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0004_fine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationhistory',
            name='review_rate',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], help_text='Review rate from 1 to 5', null=True),
        ),
        migrations.AlterField(
            model_name='reservationhistory',
            name='review_text',
            field=models.TextField(blank=True, help_text='Review text about the park', null=True),
        ),
    ]
