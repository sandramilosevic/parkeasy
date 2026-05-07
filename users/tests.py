from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='password123'
        )

        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='password123',
            is_staff=True
        )

        self.url_list = reverse('user-list')
        self.regular_user_url = reverse(
            'user-detail', kwargs={'pk': self.regular_user.id})
        self.admin_user_url = reverse(
            'user-detail', kwargs={'pk': self.admin_user.id})

    def test_unauthenticated_can_register(self):
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'pass123',
            'user_type': 'driver',
            'phone_number': '123455'
        }
        new_user = self.client.post(self.url_list, data)
        self.assertEqual(new_user.status_code, 201)

    def test_unauthenticated_cannot_see_users_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 401)

    def test_list_forbidden_for_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 403)

    def test_list_allowed_for_admin(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_own_profile(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.get(self.regular_user_url)
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_see_other_profile(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.get(self.admin_user_url)
        self.assertEquals(response.status_code, 404)

    def test_user_can_update_own_profile(self):
        self.client.force_authenticate(self.regular_user)
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'user_type': 'owner',
            'phone_number': '123455'
        }
        response = self.client.put(self.regular_user_url, data)
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_update_other_profile(self):
        self.client.force_authenticate(self.regular_user)
        data = {
            'username': 'admin',
            'email': 'admin@test.com',
            'password': 'password123',
            'is_staff': False
        }
        response = self.client.put(self.admin_user_url, data)
        self.assertEqual(response.status_code, 404)

    def test_admin_can_update_any_profile(self):
        self.client.force_authenticate(self.admin_user)
        data = {'username': 'newname'}
        response = self.client.patch(self.regular_user_url, data)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_delete_any_profile(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.delete(self.regular_user_url)
        self.assertEqual(response.status_code, 204)

    def test_user_cannot_delete_other_profile(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.delete(self.admin_user_url)
        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_own_profile(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.delete(self.regular_user_url)
        self.assertEqual(response.status_code, 204)

    def test_register_creates_user_in_db(self):
        data = {
            'username': 'registeruser',
            'email': 'registeruser@test.com',
            'password': 'password123',
            'user_type': 'owner',
            'phone_number': '061616161'
        }
        self.client.post(self.url_list, data)
        filtering_user = User.objects.filter(username='registeruser').exists()
        self.assertTrue(filtering_user)

    def test_register_password_is_hashed(self):
        data = {
            'username': 'registeruser',
            'email': 'registeruser@test.com',
            'password': 'password123',
            'user_type': 'owner',
            'phone_number': '061616161'
        }
        self.client.post(self.url_list, data)
        user = User.objects.get(username='registeruser')
        self.assertNotEqual(user.password, 'password123')
