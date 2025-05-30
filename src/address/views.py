import jwt
from rest_framework import status

from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from address.models import Address
from address.serializers import AddressSerializer
from accounts.models import User
from address.token_service import get_token


class UserAddressView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AllowAny]

    def _decode_token(self):
        token = get_token(self.request)
        return jwt.decode(token, options={"verify_signature": False})

    def create(self, request, *args, **kwargs):
        decoded = self._decode_token()

        user_id_token = decoded["sub"]
        user_id = request.data.get('user')
        user_id_db = User.objects.get(pk=user_id).auth0_id

        if user_id_token == user_id_db:
            if Address.objects.filter(user=user_id).exists():
                return Response({'message': "User can only have one address."}, status=status.HTTP_400_BAD_REQUEST)
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'Unauthorized access. '
                                        'You are trying to create an address for another user.'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None, *args, **kwargs):
        decoded = self._decode_token()

        address = Address.objects.get(pk=pk)
        user_id_token = decoded["sub"]
        user_id_db = address.user.auth0_id

        if user_id_token == user_id_db:
            kwargs['partial'] = True
            return super().update(request, *args, **kwargs)
        else:
            return Response({'message': 'Unauthorized access.'
                                        'You are trying to update an address that is not yours.'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        decoded = self._decode_token()

        address = Address.objects.get(pk=pk)
        user_id_token = decoded["sub"]
        user_id_db = address.user.auth0_id

        if user_id_token == user_id_db:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({'message': 'Unauthorized access.'}, status=status.HTTP_401_UNAUTHORIZED)
