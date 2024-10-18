from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('carts', views.fashionMallCartViewSet, basename='carts')

urlpatterns = [
    *router.urls
]