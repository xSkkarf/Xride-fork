
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class XrideUser(AbstractUser):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    national_id = models.CharField(max_length=14, unique=True, blank=True, null=True)  # National ID field

    # Override related names to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='xrideuser_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='xrideuser_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return f"Name:{self.username} Balance:{self.wallet_balance}"

class Car(models.Model):
    DOOR_STATUS_CHOICES = [
        ('locked', 'Locked'),
        ('unlocked', 'Unlocked'),
    ]

    RESERVATION_STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('available', 'Available'),
    ]

    car_name = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=20, unique=True)
    year = models.PositiveIntegerField()
    door_status = models.CharField(max_length=10, choices=DOOR_STATUS_CHOICES, default='locked')
    temperature = models.FloatField()  # Celsius temperature
    location_latitude = models.FloatField()
    location_longitude = models.FloatField()
    reservation_status = models.CharField(max_length=10, choices=RESERVATION_STATUS_CHOICES, default='available')
    booking_price_2H = models.DecimalField(max_digits=8, decimal_places=2)
    booking_price_6H = models.DecimalField(max_digits=8, decimal_places=2)
    booking_price_12H = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"ID: {self.id} Name: {self.car_name} - Year: {self.year} - Temp: {self.temperature} - status: {self.reservation_status}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PLAN_CHOICES = [
        ('2H', '2 Hours'),
        ('6H', '6 Hours'),
        ('12H', '12 Hours'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)  # Will be set when releasing the reservation
    reservation_plan = models.CharField(max_length=3, choices=PLAN_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    duration = models.FloatField(null=True, blank=True)  # Duration in hours
    def __str__(self):
        return f"{self.user.username} - {self.car.car_name} ({self.status})"
