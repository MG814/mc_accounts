import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from urllib.parse import urlparse, parse_qs

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

    def test_login_url_contains_required_parameters(self):
        response = self.client.get(self.login_url)
        login_url = response.data['login_url']

        parsed_url = urlparse(login_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('response_type', query_params)
        self.assertIn('client_id', query_params)
        self.assertIn('redirect_uri', query_params)
        self.assertIn('scope', query_params)
        self.assertIn('audience', query_params)

        self.assertEqual(query_params['response_type'][0], 'code')
        self.assertEqual(query_params['client_id'][0], settings.AUTH0_CLIENT_ID)
        self.assertEqual(query_params['redirect_uri'][0], settings.AUTH0_CALLBACK_URL)
        self.assertEqual(query_params['scope'][0], 'openid email profile')
        self.assertEqual(query_params['audience'][0], settings.AUTH0_AUDIENCE)

    def test_logout_view_returns_auth0_url(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('logout_url', response.data)
        self.assertTrue(response.data['logout_url'].startswith(f'https://{settings.AUTH0_DOMAIN}/v2/logout'))

    def test_logout_clears_session(self):
        session = self.client.session
        session['user_id'] = 'test_user_123'
        session['some_data'] = 'test_data'
        session.save()

        self.assertIn('user_id', self.client.session)
        self.assertIn('some_data', self.client.session)

        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(self.client.session.keys()), 0)

    def test_logout_url_contains_required_parameters(self):
        response = self.client.get(self.logout_url)
        logout_url = response.data['logout_url']

        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('client_id', query_params)
        self.assertIn('returnTo', query_params)

        self.assertEqual(query_params['client_id'][0], settings.AUTH0_CLIENT_ID)
        self.assertEqual(query_params['returnTo'][0], settings.LOGOUT_REDIRECT_URL)

    def test_logout_works_without_existing_session(self):
        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('logout_url', response.data)

    def test_register_view_returns_auth0_url(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('registration_url', response.data)
        self.assertTrue(response.data['registration_url'].startswith(f'https://{settings.AUTH0_DOMAIN}/authorize'))
        self.assertIn('screen_hint=signup', response.data['registration_url'])

    def test_register_url_contains_required_parameters(self):
        response = self.client.get(self.register_url)
        register_url = response.data['registration_url']

        parsed_url = urlparse(register_url)
        query_params = parse_qs(parsed_url.query)

        self.assertIn('response_type', query_params)
        self.assertIn('client_id', query_params)
        self.assertIn('redirect_uri', query_params)
        self.assertIn('scope', query_params)
        self.assertIn('audience', query_params)
        self.assertIn('screen_hint', query_params)

        self.assertEqual(query_params['response_type'][0], 'code')
        self.assertEqual(query_params['client_id'][0], settings.AUTH0_CLIENT_ID)
        self.assertEqual(query_params['redirect_uri'][0], settings.AUTH0_CALLBACK_URL)
        self.assertEqual(query_params['scope'][0], 'openid email profile')
        self.assertEqual(query_params['audience'][0], settings.AUTH0_AUDIENCE)
        self.assertEqual(query_params['screen_hint'][0], 'signup')

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
