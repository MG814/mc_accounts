from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class TestAccountsViews(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register-list")
        self.login_url = reverse("token_obtain_pair")

        self.user_data = {
                "username": "testuser",
                "email": "testuser@example.com",
                "first_name": "User",
                "last_name": "Test",
                "password": "testpassword123",
                "password_confirmation": "testpassword123",
                "phone": "123456789",
                "role": "Patient"
            }

        self.user_data_2 = {
                "username": "testuser2",
                "email": "testuser@example.com",
                "first_name": "User",
                "last_name": "Test",
                "password": "testpassword123",
                "password_confirmation": "testpassword123",
                "phone": "123456789",
                "role": "Patient",
                "specialization": "Test"
            }

        self.user_data_3 = {
                "username": "testuser3",
                "email": "testuser@example.com",
                "first_name": "User",
                "last_name": "Test",
                "password": "testpassword123",
                "password_confirmation": "testpassword123",
                "phone": "123456789",
                "role": "Doctor"
            }

        self.user_data_login = {
            "username": "testuser",
            "password": "testpassword123",
        }

    def test_register_view_success(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(reverse("register-list"), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_register_view_patient_specialization(self):
        response = self.client.post(reverse("register-list"), data=self.user_data_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Only doctors can have a specialization.", response.data["specialization"])

    def test_register_view_no_doctor_specialization(self):
        response = self.client.post(reverse("register-list"), data=self.user_data_3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Specialization is required for doctors.", response.data["specialization"])

    def test_register_user_missing_data(self):
        data = {
            "username": "new_user"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view(self):
        self.client.post(self.register_url, data=self.user_data)

        response = self.client.post(self.login_url, self.user_data_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)