import requests
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock

from accounts.models import User

from rest_framework.test import APITestCase
from accounts.views import UpdateUserView


class TestUpdateUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            auth0_id='auth0|123456',
            username='testuser',
            name='testusername',
            email='test@example.com'
        )
        self.update_user_url = reverse('update-auth0-user', kwargs={'auth0_id': self.user.auth0_id})

    @patch("requests.patch")
    @patch("requests.post")
    def test_update_user_success(self, mock_token_request, mock_auth0_patch):
        update_data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }

        mock_token_request.return_value.json.return_value = {
            'access_token': 'fake_token'
        }

        mock_auth0_patch.return_value.status_code = status.HTTP_200_OK

        response = self.client.patch(self.update_user_url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User updated.')

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')

    @patch("requests.patch")
    @patch("requests.post")
    def test_update_user_auth0_error(self, mock_token_request, mock_auth0_patch):
        update_data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }

        mock_token_request.return_value.json.return_value = {
            'access_token': 'fake_token'
        }

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
        self.assertEqual(response.data['error'], 'Authentication error with Auth0')

    def test_add_data_from_request_function(self):
        update_data = {
            'username': 'newusername',
            'name': 'newname'
        }
        view = UpdateUserView()
        local_db_data, auth0_data = view.add_data_from_request(update_data)

        self.assertEqual(local_db_data, update_data)
        self.assertEqual(auth0_data['username'], update_data['username'])
        self.assertEqual(auth0_data['user_metadata']['name'], update_data['name'])

    def test_set_new_velue_to_user(self):
        local_db_data = {
            'username': 'newusername',
            'name': 'newname'
        }
        view = UpdateUserView()
        view.set_new_value_to_user(local_db_data, self.user.auth0_id)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.name, 'newname')
