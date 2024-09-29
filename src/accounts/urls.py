from django.urls import path
from .views import (RegisterUserView, CustomTokenObtainPairView, VerifyTokenView, UserDetailView,
                    UserListView)
from rest_framework import routers

router = routers.SimpleRouter()
router.register('register', RegisterUserView, basename='register')
router.register('users', UserDetailView, basename='users-detail')
urlpatterns = [
    path('login/create-token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('users/list/', UserListView.as_view(), name='users'),
    path('users/verify-token/', VerifyTokenView.as_view(), name='user-verify'),
]
urlpatterns += router.urls
