# Generated by Django 5.1.1 on 2024-11-09 23:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride_V3', '0020_fine'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('reservation_created', 'Reservation Created'), ('reservation_updated', 'Reservation Updated'), ('reservation_deleted', 'Reservation Deleted'), ('payment_made', 'Payment Made'), ('profile_updated', 'Profile Updated'), ('fine_paid', 'Fine Paid'), ('car_booked', 'Car Booked'), ('car_returned', 'Car Returned'), ('violation_reported', 'Violation Reported')], max_length=50)),
                ('action_details', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
