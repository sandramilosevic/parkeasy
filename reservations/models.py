from django.db import models
from users.models import User
from parkings.models import Parking


class Reservation(models.Model):
    # --- Constants ---
    ACTIVE = 'active'
    FINISHED = 'finished'
    CANCELED = 'canceled'

    STATUS_CHOICE = [
        (ACTIVE, 'Active'),
        (FINISHED, 'Finished'),
        (CANCELED, 'Canceled')
    ]

    # Period type
    HOURLY = 'hourly'
    DAILY = 'daily'
    MONTHLY = 'monthly'

    PERIOD_CHOICES = [
        (HOURLY, 'Per Hour'),
        (DAILY, 'Per Day'),
        (MONTHLY, 'Per Month'),
    ]

    # --- Fields ---
    reservation_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICE,
        default=ACTIVE
    )

    period_type = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        default=HOURLY
    )

    reservation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_reservation = models.ForeignKey(Parking, on_delete=models.CASCADE)

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    full_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    # --- Methods ---
    def __str__(self):
        return f'{self.reservation_user} - {self.parking_reservation}'
