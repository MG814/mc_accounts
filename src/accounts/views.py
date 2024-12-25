from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserCreateSerializer, UserSerializer


class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Token is valid', 'current_user_role': request.user.role,
                         'current_user_id': request.user.id}, status=status.HTTP_200_OK)


class RegisterUserView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserDetailView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
