from django.contrib import admin
from reservations.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_status', 'period_type', 'reservation_user',
                    'parking_reservation', 'date_start', 'date_end', 'full_price']
    search_fields = ['reservation_user__username',
                     'parking_reservation__title', 'date_start', 'date_end']
    list_filter = ['reservation_status', 'period_type']
    ordering = ['date_start', 'date_end']
