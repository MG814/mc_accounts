from django.urls import path
from rest_framework import routers

from .views import UserAddressView

router = routers.SimpleRouter()
router.register('users', UserAddressView, basename='user-addresss')


urlpatterns = [
]

urlpatterns += router.urls
