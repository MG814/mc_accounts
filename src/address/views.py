from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from address.models import Address
from address.serializers import AddressSerializer


class UserAddressView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Zwracamy tylko adresy powiązane z zalogowanym użytkownikiem
        user = self.request.user
        return Address.objects.filter(user=user)

    # Zwrócenie adresu zalogowanego użytkownika
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        try:
            address = queryset.get()  # Szukamy adresu użytkownika
        except Address.DoesNotExist:
            raise NotFound(detail="Address not found", code=404)

        serializer = self.get_serializer(address)
        return Response(serializer.data)

    # Aktualizacja lub utworzenie adresu
    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        try:
            address = queryset.get()
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(address, data=request.data, partial=partial)
        except Address.DoesNotExist:
            # Jeśli adres nie istnieje, tworzymy nowy
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
