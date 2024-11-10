# Generated by Django 5.1.1 on 2024-11-10 00:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0026_delete_reservationhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_ID', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('reservation_plan', models.CharField(choices=[('2H', '2 Hours'), ('6H', '6 Hours'), ('12H', '12 Hours')], max_length=3)),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('cancelled', 'Cancelled')], default='completed', max_length=10)),
                ('duration', models.FloatField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride_V3.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
    ]
