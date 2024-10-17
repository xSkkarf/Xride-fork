import hashlib
import hmac
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import F
from rest_framework import generics
from .models import *
from .serializers import *
from django.utils import timezone
from math import radians, cos, sin, asin, sqrt
from datetime import datetime


def calculate_duration_in_hours(start_time: datetime, end_time: datetime) -> float:
    duration = end_time - start_time  # Calculate duration as a timedelta
    duration_in_hours = duration.total_seconds() / 3600  # Convert seconds to hours
    return round(duration_in_hours,4)

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth radius in km
    return c * r

class UserDetailView(generics.RetrieveAPIView):
    queryset = XrideUser.objects.all()
    serializer_class = XrideUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Return the current authenticated user

class AvailableCarsWithinRadiusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_lat = request.query_params.get('latitude')
        user_lon = request.query_params.get('longitude')

        if not user_lat or not user_lon:
            return Response({'error': 'Please provide valid latitude and longitude.'}, status=status.HTTP_400_BAD_REQUEST)

        user_lat = float(user_lat)
        user_lon = float(user_lon)

        # Fetch cars with minimal data needed (no full object fetch)
        cars = Car.objects.filter(reservation_status='available').only('id', 'location_latitude', 'location_longitude')
        
        nearby_cars = [
            CarSerializer(car).data for car in cars
            if haversine(user_lon, user_lat,car.location_longitude,car.location_latitude ) <= 2
        ]

        return Response({'nearby_cars': nearby_cars}, status=status.HTTP_200_OK)
    
class ReserveCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, car_id):
        user = request.user
        reservation_plan = request.data.get('reservation_plan')  # Expecting '2H', '6H', or '12H'

        # Check if the car exists
        car = Car.objects.filter(id=car_id).first()
        if not car:
            return Response({"error": "Car not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has an active reservation
        active_reservation = Reservation.objects.filter(user=user, status='active').first()
        if active_reservation:
            return Response({"error": "You already have an active reservation."}, status=status.HTTP_400_BAD_REQUEST)

        # Check car availability
        if car.reservation_status != 'available':
            return Response({"error": "Car is already reserved or unavailable."}, status=status.HTTP_400_BAD_REQUEST)

        # Create reservation
        reservation = Reservation.objects.create(
            user=user,
            car=car,
            reservation_plan=reservation_plan,
            start_time=timezone.now()  # Set start time to the current time
        )
        
        # Update car reservation status
        car.reservation_status = 'reserved'
        car.save(update_fields=['reservation_status'])

        return Response({"message": f"You have successfully reserved {car.car_name}.", "reservation_id": reservation.id}, status=status.HTTP_200_OK)

class ReleaseCarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, car_id):
        user = request.user

        # Check if the car exists
        car = Car.objects.filter(id=car_id).first()
        if not car:
            return Response({"error": "Car not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the car is reserved by the current user
        reservation = Reservation.objects.filter(user=user, car=car, status='active').first()
        if not reservation:
            return Response({"error": "You do not have a reservation for this car."}, status=status.HTTP_403_FORBIDDEN)

        # Set the reservation status to completed
        reservation.status = 'completed'
        reservation.end_time = timezone.now()  # Set the end time to now
        reservation.duration = calculate_duration_in_hours(reservation.start_time, reservation.end_time)
        reservation.save()

        # Set the car status to available
        car.reservation_status = 'available'
        car.save(update_fields=['reservation_status'])

        return Response({
            "message": f"You have successfully released {car.car_name}.",
            "duration_hours": reservation.duration  # Return the duration
        }, status=status.HTTP_200_OK)

class UserListReservationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        reservations = Reservation.objects.filter(user=user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CarStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, car_id):
        try:
            car = Car.objects.get(pk=car_id)
            active_reservation = Reservation.objects.filter(user=request.user, car=car, status='active').first()
            if not active_reservation:
                return Response({'error': 'You do not have an active reservation for this car'}, status=status.HTTP_403_FORBIDDEN)
            serializer = CarSerializer(car)
            return Response(serializer.data)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

class DoorStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, car_id):
        try:
            car = Car.objects.get(pk=car_id)
            active_reservation = Reservation.objects.filter(user=request.user, car=car, status='active').first()
            if not active_reservation:
                return Response({'error': 'You do not have an active reservation for this car'}, status=status.HTTP_403_FORBIDDEN)
            if car.door_status == 'unlocked':
                car.door_status = 'locked'
                status_message = 'Door locked successfully.'
            else:
                car.door_status = 'unlocked'
                status_message = 'Door unlocked successfully.'
            car.save()  # Save the updated status
            return Response({'status': status_message})
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)


class EchoView(APIView):
    """Echoes back the POST request body as JSON."""
    
    def post(self, request):
        # Get the request data
        data = request.data
        if not data:
            return Response({'error': "nothing"}, status=status.HTTP_200_OK)
        
        data = data["obj"]
        received_hmac = request.query_params.get('hmac')
        
         # Define the order of keys for HMAC calculation
        hmac_keys = [
            'amount_cents', 'created_at', 'currency', 'error_occured', 'has_parent_transaction', 'id',
            'integration_id', 'is_3d_secure', 'is_auth', 'is_capture', 'is_refunded', 'is_standalone_payment',
            'is_voided', 'order.id', 'owner', 'pending', 'source_data.pan', 'source_data.sub_type',
            'source_data.type', 'success'
        ]

        # Sort the data by key and concatenate the values in the specified order
        concatenated_string = self.generate_hmac_string(data, hmac_keys)

        print("concatenated_string",concatenated_string)

        # Calculate the HMAC using SHA512 and your HMAC secret
        secret = "D229E5A90A84B96B8ACAAD3ADF2BE93C"
        calculated_hmac = hmac.new(secret.encode(), concatenated_string.encode(), hashlib.sha512).hexdigest()

        print("calculated_hmac",calculated_hmac)
        print("received_hmac",received_hmac)
        # Compare the calculated HMAC with the received HMAC
        if calculated_hmac != received_hmac:
            return Response({'error': 'Invalid HMAC'}, status=status.HTTP_403_FORBIDDEN)

        print("HMAC is valid")
        # Return the data as the response
        return Response(data, status=status.HTTP_200_OK)
    
    def get_nested_value(self, data, key):
        keys = key.split('.')
        for k in keys:
            data = data.get(k, {})
        return data
    
    def generate_hmac_string(self, data, keys):
        hmac_string = ''
        for key in keys:
            value = self.get_nested_value(data, key)
            if value in (True, False):
                value = str(value).lower()
            hmac_string += str(value)
        return hmac_string
