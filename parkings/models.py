from django.db import models
from users.models import User


class Parking(models.Model):
    # --- Constants ---

    # Parking type
    OPEN_LOT = 'open_lot'
    GARAGE = 'garage'
    OTHER = 'other'

    PARKING_TYPE_CHOICES = [
        (OPEN_LOT, 'open lot'),
        (GARAGE, 'garage'),
        (OTHER, 'other')
    ]
    # Distance from center
    CENTER = 'center'
    NEAR = 'near'        # up to 500m
    FAR = 'far'          # up to 1km
    VERY_FAR = 'very_far'  # over 1km

    DISTANCE_CHOICES = [
        (CENTER, 'In Center'),
        (NEAR, 'Up to 500m'),
        (FAR, 'Up to 1km'),
        (VERY_FAR, 'Over 1km')
    ]

    # --- Fields ---

    title = models.CharField(max_length=100)

    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2)

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    description = models.TextField()

    image = models.URLField(blank=True)
    featured = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    parking_type = models.CharField(
        max_length=20,
        choices=PARKING_TYPE_CHOICES,
        default=OPEN_LOT
    )

    distance = models.CharField(
        max_length=20,
        choices=DISTANCE_CHOICES,
        default=CENTER
    )

    # --- Methods ---
    def __str__(self):
        return self.title
