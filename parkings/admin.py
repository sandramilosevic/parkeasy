from django.contrib import admin
from parkings.models import Parking


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'price_per_hour', 'owner']
    search_fields = ['title', 'city']
    list_filter = ['city', 'parking_type']

    ordering = ['-price_per_hour']
