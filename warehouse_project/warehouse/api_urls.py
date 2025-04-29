from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'supplies', api_views.SupplyViewSet)
router.register(r'shipments', api_views.ShipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
