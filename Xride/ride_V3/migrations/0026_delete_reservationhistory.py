# Generated by Django 5.1.1 on 2024-11-10 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0025_reservationhistory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReservationHistory',
        ),
    ]