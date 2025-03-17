from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError

from address.models import Address
from address.serializers import AddressSerializer


class UserAddressView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin):
    serializer_class = AddressSerializer
    permission_classes = [AllowAny]
    queryset = Address.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if Address.objects.filter(user=user).exists():
            raise ValidationError("User can only have one address.")

        serializer.save(user=user)
