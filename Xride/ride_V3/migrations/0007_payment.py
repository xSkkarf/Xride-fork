# Generated by Django 5.1.1 on 2024-10-17 13:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0006_alter_reservation_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50, unique=True)),
                ('order_id', models.CharField(max_length=50)),
                ('amount_cents', models.PositiveIntegerField()),
                ('currency', models.CharField(default='EGP', max_length=5)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('is_captured', models.BooleanField(default=False)),
                ('is_refunded', models.BooleanField(default=False)),
                ('is_voided', models.BooleanField(default=False)),
                ('card_type', models.CharField(blank=True, max_length=20, null=True)),
                ('card_last_digits', models.CharField(blank=True, max_length=4, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
