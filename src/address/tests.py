from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Address
from .serializers import AddressSerializer
from .factory_models import AddressFactory
from accounts.factory_models import UserFactory


class UserAddressViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.address_url = reverse('address-list')
        self.address = AddressFactory()

    def test_create_address(self):
        data = {
            'user': self.user.id,
            'locality': 'Warszawa',
            'street': 'Ulica Testowa',
            'zip_code': '00-000'
        }
        self.assertEqual(Address.objects.filter(user=self.user.id).count(), 0)
        response = self.client.post(self.address_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.filter(user=self.user.id).count(), 1)

    def test_create_multiple_addresses(self):
        AddressFactory()

        data = {
            'locality': 'Kraków',
            'street': 'Inna Ulica',
            'zip_code': '30-000'
        }
        response = self.client.post(self.address_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaisesMessage(ValidationError, "User can only have one address.")

    def test_get_address(self):
        response = self.client.get(reverse('address-detail', args=[self.address.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, AddressSerializer(self.address).data)

    def test_update_address(self):
        update_data = {
            'locality': 'Kraków',
            'street': 'Nowa Ulica',
            'zip_code': '30-000'
        }
        response = self.client.patch(reverse('address-detail', args=[self.address.id]), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address.refresh_from_db()

        self.assertEqual(self.address.locality, 'Kraków')
        self.assertEqual(self.address.street, 'Nowa Ulica')
