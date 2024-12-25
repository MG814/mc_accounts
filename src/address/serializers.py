from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['user', 'locality', 'street', 'zip_code']

    def validate_zip_code(self, value: str):
        if len(value) != 6:
            raise serializers.ValidationError("Invalid zip code format. It should be 6 characters long.")
        return value
