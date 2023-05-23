from django.urls import include, path
from rest_framework import routers

from api.views import BasketItemModelViewSet, ProductModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'basket-items', BasketItemModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
