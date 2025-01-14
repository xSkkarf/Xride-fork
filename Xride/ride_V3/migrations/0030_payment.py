# Generated by Django 5.1.1 on 2024-11-11 02:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0029_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('order_id', models.TextField(unique=True)),
                ('collector', models.CharField(blank=True, max_length=255, null=True)),
                ('card_type', models.CharField(blank=True, max_length=20, null=True)),
                ('card_last_four', models.CharField(blank=True, max_length=4, null=True)),
                ('currency', models.CharField(blank=True, max_length=3, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('txn_response_code', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
