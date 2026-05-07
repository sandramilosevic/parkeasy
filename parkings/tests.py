from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from parkings.models import Parking
from django.urls import reverse


class ParkingTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner_user = User.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='password123',
            user_type='owner'
        )

        self.driver_user = User.objects.create_user(
            username='driver',
            email='driver@test.com',
            password='password123',
            user_type='driver'
        )

        self.url_list = reverse('parking-list')

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

        self.parking_url = reverse(
            'parking-detail', kwargs={'pk': self.parking.id})

    # --- Authentication ---

    def test_unauthenticated_cannot_create_parking(self):
        data = {
            'title': 'Parking Testing',
            'price_per_hour': 1.00,
            'price_per_day': 17.00,
            'price_per_month': 70.00,
            'address': 'Tests Address',
            'city': 'Test City',
            'description': 'Description',
        }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, 401)

    # --- Read ---

    def test_anyone_can_see_parking_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

    # --- Create ---

    def test_owner_can_create_parking(self):
        self.client.force_authenticate(self.owner_user)
        data = {
            'title': 'Parking',
            'price_per_hour': 1.00,
            'price_per_day': 17.00,
            'price_per_month': 70.00,
            'address': 'Test Address',
            'city': 'Test City',
            'description': 'Description'
        }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, 201)

    def test_driver_cannot_create_parking(self):
        self.client.force_authenticate(self.driver_user)
        data = {
            'title': 'Parking',
            'price_per_hour': 1.00,
            'price_per_day': 17.00,
            'price_per_month': 70.00,
            'address': 'Test Address',
            'city': 'Test City',
            'description': 'Description',
        }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, 403)

    # --- Update ---

    def test_owner_can_update_own_parking(self):
        self.client.force_authenticate(self.owner_user)
        data = {'price_per_hour': 2.00}
        response = self.client.patch(self.parking_url, data)
        self.assertEqual(response.status_code, 200)

    def test_driver_cannot_update_parking(self):
        self.client.force_authenticate(self.driver_user)
        data = {'price_per_hour': 2.25}
        response = self.client.patch(self.parking_url, data)
        self.assertEqual(response.status_code, 403)

    # --- Delete ---

    def test_owner_can_delete_own_parking(self):
        self.client.force_authenticate(self.owner_user)
        response = self.client.delete(self.parking_url)
        self.assertEqual(response.status_code, 204)

    def test_driver_cannot_delete_parking(self):
        self.client.force_authenticate(self.driver_user)
        response = self.client.delete(self.parking_url)
        self.assertEqual(response.status_code, 403)
