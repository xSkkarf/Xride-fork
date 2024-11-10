# Generated by Django 5.1.1 on 2024-11-09 22:49

import django.db.models.deletion
import ride_V3.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0019_reservation_reservationhistory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending'), ('unpaid', 'Unpaid')], default='pending', max_length=20)),
                ('violation_copy', models.ImageField(blank=True, null=True, upload_to=ride_V3.models.violation_photo_upload_path)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride_V3.car')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride_V3.reservation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
