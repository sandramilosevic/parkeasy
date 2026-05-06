from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Reservation
from parkings.models import Parking
from decimal import Decimal


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id',
            'reservation_status',
            'reservation_user',
            'parking_reservation',
            'period_type',
            'date_start',
            'date_end',
            'date_created',
            'full_price',
        ]
        # These fields are set automatically, user should not be able to change them
        read_only_fields = ['reservation_user',
                            'date_created', 'full_price', 'reservation_status']

    # validate is called automatically before saving to check if data is correct

    def validate(self, data):

        date_start = data['date_start']
        date_end = data['date_end']

        if not date_start or not date_end:
            return data

        # End time must be after start time
        if date_end <= date_start:
            raise serializers.ValidationError(
                'End date must be after start date.')

        # Minimum reservation duration is 1 hour
        if date_end - date_start < timedelta(hours=1):
            raise serializers.ValidationError(
                'Reservation must be at least 1 hour.')
        return data

    # create is called when user sends POST request to create a reservation
    def create(self, validated_data):

        parking = validated_data['parking_reservation']

        date_start = validated_data['date_start']
        date_end = validated_data['date_end']

        period_type = validated_data['period_type']

        # Calculate total duration of reservation
        duration = date_end - date_start

        if period_type == Reservation.HOURLY:
            numbers_of_hours = duration.total_seconds() / 3600
            validated_data['full_price'] = parking.price_per_hour * \
                Decimal(str(numbers_of_hours))

        elif period_type == Reservation.DAILY:
            numbers_of_days = duration.total_seconds() / 86400
            validated_data['full_price'] = parking.price_per_day * \
                Decimal(str(numbers_of_days))

        elif period_type == Reservation.MONTHLY:
            numbers_of_months = duration.days / 30
            validated_data['full_price'] = parking.price_per_month * \
                Decimal(str(numbers_of_months))

        return super().create(validated_data)
