# Generated by Django 5.1.1 on 2024-10-17 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0007_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='card_last_digits',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='card_type',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='is_captured',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='is_refunded',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='is_voided',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='updated_at',
        ),
    ]
