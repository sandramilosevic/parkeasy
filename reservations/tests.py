from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from parkings.models import Parking
from .models import Reservation
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class ReservationsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.driver_user = User.objects.create_user(
            username='driver',
            email='driver@test.com',
            password='password123',
            user_type='driver'
        )

        self.driver_user2 = User.objects.create_user(
            username='driver2',
            email='driver2@test.com',
            password='password123',
            user_type='driver'
        )

        self.owner_user = User.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='password123',
            user_type='owner'
        )

        self.parking = Parking.objects.create(
            title='Test Parking',
            price_per_hour=1.00,
            price_per_day=17.00,
            price_per_month=70.00,
            address='Test Address',
            city='Test City',
            description='Test Description',
            owner=self.owner_user
        )

        self.reservation = Reservation.objects.create(
            reservation_user=self.driver_user,
            parking_reservation=self.parking,
            date_start=timezone.now(),
            date_end=timezone.now() + timedelta(hours=2),
            period_type='hourly'
        )

        self.reservation_driver2 = Reservation.objects.create(
            reservation_user=self.driver_user2,
            parking_reservation=self.parking,
            date_start=timezone.now(),
            date_end=timezone.now() + timedelta(hours=2),
            period_type='hourly'
        )

        self.reservation_data = {
            'parking_reservation': self.parking.id,
            'date_start': timezone.now() + timedelta(hours=1),
            'date_end': timezone.now() + timedelta(hours=3),
            'period_type': 'hourly'
        }

        self.urls_list = reverse('reservation-list')

        self.reservation_url = reverse(
            'reservation-detail', kwargs={'pk': self.reservation.id})

        self.reservation_driver2_url = reverse(
            'reservation-detail', kwargs={'pk': self.reservation_driver2.id})

    # --- Authentication ---

    def test_unauthenticated_cannot_see_reservations(self):
        response = self.client.get(self.urls_list)
        self.assertEqual(response.status_code, 401)

    # --- Create ---

    def test_driver_can_create_reservation(self):
        self.client.force_authenticate(self.driver_user)
        response = self.client.post(self.urls_list, self.reservation_data)
        self.assertEqual(response.status_code, 201)

    def test_owner_cannot_create_reservation(self):
        self.client.force_authenticate(self.owner_user)
        response = self.client.post(self.urls_list, self.reservation_data)
        self.assertEqual(response.status_code, 403)

    def test_reservation_user_set_automatically(self):
        self.client.force_authenticate(self.driver_user)
        response = self.client.post(self.urls_list, self.reservation_data)
        self.assertEqual(response.status_code, 201)
        reservation = Reservation.objects.get(id=response.data['id'])
        self.assertEqual(reservation.reservation_user, self.driver_user)

    def test_reservation_default_status_is_active(self):
        self.client.force_authenticate(self.driver_user)
        response = self.client.post(self.urls_list, self.reservation_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['reservation_status'], 'active')

    def test_user_cannot_set_full_price_manually(self):
        self.client.force_authenticate(self.driver_user)
        data = {**self.reservation_data, 'full_price': '999.00'}
        response = self.client.post(self.urls_list, data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(
            Decimal(response.data['full_price']), Decimal('999.00'))

    # --- Read ---

    def test_driver_can_see_own_reservation(self):
        self.client.force_authenticate(self.driver_user)
        response = self.client.get(self.reservation_url)
        self.assertEqual(response.status_code, 200)

    def test_driver_cannot_see_other_driver_reservations(self):
        self.client.force_authenticate(self.driver_user2)
        response = self.client.get(self.reservation_url)
        self.assertEqual(response.status_code, 404)

    def test_driver_sees_only_own_reservation_in_list(self):
        self.client.force_authenticate(self.driver_user)
        response = self.client.get(self.urls_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.reservation.id)

    # --- Update ---

    def test_driver_can_update_own_reservation(self):
        self.client.force_authenticate(self.driver_user)
        updating = {'period_type': 'daily'}
        response = self.client.patch(self.reservation_url, updating)
        self.assertEqual(response.status_code, 200)

    def test_driver_cannot_update_other_reservation(self):
        self.client.force_authenticate(self.driver_user2)
        updating = {'period_type': 'daily'}
        response = self.client.patch(self.reservation_url, updating)
        self.assertEqual(response.status_code, 404)

    # --- Delete ---

    def test_driver_can_delete_own_reservation(self):
        self.client.force_authenticate(self.driver_user)
        response = self.client.delete(self.reservation_url)
        self.assertEqual(response.status_code, 204)

    def test_driver_cannot_delete_other_reservation(self):
        self.client.force_authenticate(self.driver_user2)
        response = self.client.delete(self.reservation_url)
        self.assertEqual(response.status_code, 404)

    # --- Price calculation ---

    def test_full_price_calculated_on_create(self):
        # 2 hours * price_per_hour=1.00 → expected 2.00
        self.client.force_authenticate(self.driver_user)
        response = self.client.post(self.urls_list, self.reservation_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Decimal(response.data['full_price']), Decimal('2.00'))

    def test_full_price_calculated_daily(self):
        # 2 days * price_per_day=17.00 → expected 34.00
        self.client.force_authenticate(self.driver_user)
        data = {
            'parking_reservation': self.parking.id,
            'date_start': timezone.now() + timedelta(hours=1),
            'date_end': timezone.now() + timedelta(days=2, hours=1),
            'period_type': 'daily'
        }
        response = self.client.post(self.urls_list, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Decimal(response.data['full_price']), Decimal('34.00'))

    # --- Validation ---

    def test_invalid_date_range(self):
        self.client.force_authenticate(self.driver_user)
        invalid_data = {
            **self.reservation_data,
            'date_start': timezone.now() + timedelta(hours=3),
            'date_end': timezone.now() + timedelta(hours=1),
        }
        response = self.client.post(self.urls_list, invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_reservation_too_short(self):
        self.client.force_authenticate(self.driver_user)
        short_data = {
            **self.reservation_data,
            'date_start': timezone.now() + timedelta(hours=1),
            'date_end': timezone.now() + timedelta(minutes=30),
        }
        response = self.client.post(self.urls_list, short_data)
        self.assertEqual(response.status_code, 400)
