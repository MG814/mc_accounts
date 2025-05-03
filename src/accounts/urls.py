from django.urls import path

from .views import UserDetailView, LoginView, RegisterUserView, LogoutView, UpdateUserView
from rest_framework import routers
router = routers.SimpleRouter()
router.register('register', RegisterUserView, basename='register')
router.register('users', UserDetailView, basename='users')

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth0-login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('update-user/<int:user_id>/', UpdateUserView.as_view(), name='update-auth0-user'),
]
urlpatterns += router.urls
