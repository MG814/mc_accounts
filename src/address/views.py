from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError

from address.models import Address
from address.serializers import AddressSerializer


class UserAddressView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    queryset = Address

    def perform_create(self, serializer):
        user = self.request.user
        if Address.objects.filter(user=user).exists():
            raise ValidationError("User can only have one address.")

        serializer.save(user=user)