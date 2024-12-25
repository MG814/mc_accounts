from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterUserView, VerifyTokenView, UserDetailView
from rest_framework import routers

router = routers.SimpleRouter()
router.register('register', RegisterUserView, basename='register')
router.register('users', UserDetailView, basename='users')
urlpatterns = [
    path('login/create-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/verify-token/', VerifyTokenView.as_view(), name='user-verify'),
]
urlpatterns += router.urls
