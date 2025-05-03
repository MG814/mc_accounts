import json
import requests

from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from urllib.parse import urlencode
from django.conf import settings

from .serializers import UserSerializer
from accounts.models import User


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        auth_params = {
            'response_type': 'code',
            'client_id': settings.AUTH0_CLIENT_ID,
            'redirect_uri': settings.AUTH0_CALLBACK_URL,
            'scope': 'openid email profile',
            'audience': settings.AUTH0_AUDIENCE,
        }
        auth_url = f"https://{settings.AUTH0_DOMAIN}/authorize?{urlencode(auth_params)}"

        return Response({'login_url': auth_url})


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        request.session.flush()

        logout_url = (
            f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
            f"client_id={settings.AUTH0_CLIENT_ID}&"
            f"returnTo={settings.LOGOUT_REDIRECT_URL}"
        )

        return Response({'logout_url': logout_url})


class RegisterUserView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        auth_params = {
            'response_type': 'code',
            'client_id': settings.AUTH0_CLIENT_ID,
            'redirect_uri': settings.AUTH0_CALLBACK_URL,
            'scope': 'openid email profile',
            'audience': settings.AUTH0_AUDIENCE,
            'screen_hint': 'signup'
        }
        auth_url = f"https://{settings.AUTH0_DOMAIN}/authorize?{urlencode(auth_params)}"
        return Response({'registration_url': auth_url})

    def create(self, request, *args, **kwargs):
        request_data = json.loads(request.body)

        User.objects.create(
            auth0_id=request_data.get('user_id'),
            username=request_data.get('username'),
            email=request_data.get('email'),
            name=request_data.get('name'),
            surname=request_data.get('surname'),
            phone=request_data.get('phone'),
            role=request_data.get('role'),
            specialization=request_data.get('specialization'),
        )

        return Response({"message": "User registered successfully", "user_id": request_data.get('user_id')},
                        status=status.HTTP_201_CREATED)


class UserDetailView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UpdateUserView(APIView):
    permission_classes = [AllowAny]

    def get_management_token(self):
        url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        payload = {
            "client_id": settings.AUTH0_CLIENT_ID,
            "client_secret": settings.AUTH0_CLIENT_SECRET,
            "audience": settings.AUTH0_AUDIENCE,
            "grant_type": "client_credentials",
        }
        response = requests.post(url, json=payload)
        response_data = response.json()

        return response_data.get("access_token")

    def add_data_from_request(self, request_data):
        fields = ['username', 'email']
        auth0_data = {}
        auth0_user_metadata = {}
        local_data_base_data = {}

        for key, value in request_data.items():
            if key in fields:
                auth0_data[key] = value
            else:
                auth0_user_metadata[key] = value
            local_data_base_data[key] = value
        auth0_data["user_metadata"] = auth0_user_metadata
        return local_data_base_data, auth0_data

    def set_new_value_to_user(self, local_data_base_data, auth0_id):
        user = User.objects.get(auth0_id=auth0_id)
        for field, value in local_data_base_data.items():
            setattr(user, field, value)
        user.save()

    def patch(self, request, user_id):
        auth0_token = self.get_management_token()
        if not auth0_token:
            return Response({"error": "Błąd autoryzacji z Auth0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        auth0_id = User.objects.get(id=user_id).auth0_id

        auth0_url = f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{auth0_id}"

        headers = {"Authorization": f"Bearer {auth0_token}", "Content-Type": "application/json"}
        local_data_base_data, auth0_data = self.add_data_from_request(request.data)

        try:
            auth0_response = requests.patch(auth0_url, json=auth0_data, headers=headers)
            auth0_response.raise_for_status()
            self.set_new_value_to_user(local_data_base_data, auth0_id)

            return Response({"message": "Użytkownik zaktualizowany"}, status=status.HTTP_200_OK)
        except requests.exceptions.HTTPError as http_err:
            return Response({
                "error": "Błąd aktualizacji użytkownika w Auth0",
                "details": http_err.response.json() if http_err.response.text else {},
                "status_code": http_err.response.status_code
            }, status=http_err.response.status_code)
