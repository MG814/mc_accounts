from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'specialization']


class UserCreateSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation',
                  'phone', 'role', 'specialization']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")

        role = data.get('role')
        specialization = data.get('specialization')

        if role == 'Doctor' and not specialization:
            raise serializers.ValidationError({"specialization": "Specialization is required for doctors."})
        if role == 'Patient' and specialization:
            raise serializers.ValidationError({"specialization": "Only doctors can have a specialization."})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')

        user = User.objects.create_user(**validated_data)
        return user
