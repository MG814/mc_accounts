from django.urls import path

from .views import UserDetailView, LoginView, RegisterUserView, LogoutView, UpdateAuth0UserView
from rest_framework import routers
router = routers.SimpleRouter()
router.register('register', RegisterUserView, basename='register')
router.register('users', UserDetailView, basename='users')

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth0-login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('update-user/<str:auth0_id>/', UpdateAuth0UserView.as_view(), name='update-auth0-user'),
]
urlpatterns += router.urls
