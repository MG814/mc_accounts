from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from accounts.factories import UserFactory


class UserDetailViewTests(APITestCase):

    def setUp(self):
        self.user = UserFactory(username='testuser', email='testuser@example.com')

        self.user_details_url = reverse('users-detail', args=[self.user.id])

    def test_user_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
