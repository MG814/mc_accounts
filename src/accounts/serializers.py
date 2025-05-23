from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'auth0_id', 'username', 'email', 'name', 'surname', 'role', 'specialization']
