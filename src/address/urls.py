from rest_framework import routers

from .views import UserAddressView

router = routers.SimpleRouter()
router.register('', UserAddressView, basename='address')

urlpatterns = router.urls
