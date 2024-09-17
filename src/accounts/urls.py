from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserView, CustomTokenObtainPairView, UserAddressView, VerifyTokenView

router = DefaultRouter()

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/create-token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('user/address/', UserAddressView.as_view(), name='user-address'),
    path('user/verify-token/', VerifyTokenView.as_view(), name='user-verify'),
]
