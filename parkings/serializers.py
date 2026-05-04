from rest_framework import serializers
from .models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = [
            'id',
            'title',
            'price_per_hour',
            'price_per_day',
            'price_per_month',
            'address',
            'city',
            'description',
            'image',
            'featured',
            'date_created',
            'owner',
            'parking_type',
            'distance',
        ]
        # owner is set automatically from logged in user
        read_only_fields = ['owner', 'date_created']
