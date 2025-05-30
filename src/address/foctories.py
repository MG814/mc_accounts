import factory

from .models import Address
from accounts.factories import UserFactory


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    user = factory.SubFactory(UserFactory)
    locality = factory.Faker('city')
    street = factory.Faker('street_name')
    zip_code = factory.Faker('postcode')
