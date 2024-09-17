from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Address
from .serializers import UserCreateSerializer


class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Jeśli użytkownik jest uwierzytelniony, zwracamy status 200
        return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)

class UserAddressView(APIView):
    # Używamy autoryzacji JWT
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Pobieramy aktualnie zalogowanego użytkownika z tokena JWT
        user = request.user

        try:
            # Zakładamy, że adres jest powiązany z modelem użytkownika
            address = Address.objects.get(user=user)
            address_data = {
                'street': address.street,
                'locality': address.locality,
                'zipcode': address.zip_code
            }
            return Response(address_data, status=status.HTTP_200_OK)

        except Address.DoesNotExist:
            return Response(
                {'error': 'Address not found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )

class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    pass
