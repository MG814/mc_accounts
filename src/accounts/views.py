from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserCreateSerializer, UserSerializer, CustomTokenObtainPairSerializer


class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Jeśli użytkownik jest uwierzytelniony, zwracamy status 200
        return Response({'message': 'Token is valid', 'current_user_role': request.user.role,
                         'current_user_id': request.user.id}, status=status.HTTP_200_OK)


class RegisterUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserDetailView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
