from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("address", views.fashionMallAddressViewSet, basename="address")
router.register("user", views.fashionMallUserAddressViewSet, basename="useraddress")

urlpatterns = [
    *router.urls
]