from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("fashionMall-ad", views.fashionMallImagesADViewSet, basename="fashionMall-ad")

urlpatterns = [
    *router.urls
]