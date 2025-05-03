from rest_framework import status

from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError

from address.models import Address
from address.serializers import AddressSerializer
from accounts.models import User


class UserAddressView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.data.get('user')
        user = User.objects.get(pk=user_id)

        if Address.objects.filter(user=user).exists():
            raise ValidationError("User can only have one address.")

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
