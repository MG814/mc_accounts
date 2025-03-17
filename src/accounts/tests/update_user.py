import requests
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock

from accounts.models import User

from rest_framework.test import APITestCase


class TestUpdateUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            auth0_id='auth0|123456',
            username='testuser',
            email='test@example.com'
        )
        self.update_user_url = reverse('update-auth0-user', kwargs={'auth0_id': self.user.auth0_id})

    @patch("requests.patch")
    @patch("requests.post")
    def test_update_user_success(self, mock_token_request, mock_auth0_patch):
        update_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'custom_field': 'custom_value'
        }
        # Symulacja pobrania tokena
        mock_token_request.return_value.json.return_value = {
            'access_token': 'fake_token'
        }

        # Symulacja sukcesu aktualizacji w Auth0
        mock_auth0_patch.return_value.raise_for_status.return_value = None

        response = self.client.patch(self.update_user_url, update_data, format='json')

        # Weryfikacja odpowiedzi
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Użytkownik zaktualizowany w Auth0')

        # Weryfikacja aktualizacji użytkownika w bazie
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')

    @patch("requests.patch")
    @patch("requests.post")
    def test_update_user_auth0_error(self, mock_token_request, mock_auth0_patch):
        # Dane do aktualizacji
        update_data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }

        mock_token_request.return_value.json.return_value = {
            'access_token': 'fake_token'
        }

        # Symulacja błędu Auth0
        mock_error_response = MagicMock()
        mock_error_response.status_code = status.HTTP_400_BAD_REQUEST
        mock_error_response.json.return_value = {
            'error': 'invalid_request',
            'error_description': 'Some Auth0 error'
        }
        mock_auth0_patch.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_error_response
        )

        response = self.client.patch(self.update_user_url, update_data, format='json')

        self.assertEqual(response.status_code, mock_error_response.status_code)
        self.assertIn('error', response.data)
        self.assertIn('details', response.data)

    @patch("requests.post")
    def test_update_user_token_failure(self, mock_token_request):
        mock_token_request.return_value.json.return_value = {}

        response = self.client.patch(self.update_user_url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Błąd autoryzacji z Auth0')