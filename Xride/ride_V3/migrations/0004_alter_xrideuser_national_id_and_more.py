# Generated by Django 5.1.1 on 2024-10-15 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0003_xrideuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xrideuser',
            name='national_id',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='xrideuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
