import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from core import settings


class TestAccountsViews(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register-list")
        self.login_url = reverse("auth0-login")
        self.logout_url = reverse("logout")

        self.user_data = {
            "user_id": "auth0|123456789",
            "username": "testuser",
            "email": "testuser@example.com",
            "name": "User",
            "surname": "Test",
            "phone": "123456789",
            "role": "Patient"
        }

        self.doctor_data = {
            "user_id": "auth0|987654321",
            "username": "doctor1",
            "email": "doctor@example.com",
            "name": "Doctor",
            "surname": "Test",
            "phone": "987654321",
            "role": "Doctor",
            "specialization": "Cardiology"
        }

    def test_login_view_returns_auth0_url(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('login_url', response.data)
        self.assertTrue(response.data['login_url'].startswith(f'https://{settings.AUTH0_DOMAIN}/authorize'))

    def test_logout_view_returns_auth0_url(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('logout_url', response.data)
        self.assertTrue(response.data['logout_url'].startswith(f'https://{settings.AUTH0_DOMAIN}/v2/logout'))

    def test_register_view_returns_auth0_url(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('registration_url', response.data)
        self.assertTrue(response.data['registration_url'].startswith(f'https://{settings.AUTH0_DOMAIN}/authorize'))
        self.assertIn('screen_hint=signup', response.data['registration_url'])

    def test_create_user_success(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(
            self.register_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.auth0_id, "auth0|123456789")

    def test_create_doctor_success(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(
            self.register_url,
            data=json.dumps(self.doctor_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.role, "Doctor")
        self.assertEqual(user.specialization, "Cardiology")