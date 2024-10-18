from django.urls import path

from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(
    "comment", 
    views.fashionMallCommentViewSet, 
    basename="comment"
)

urlpatterns = [
    path(
        'spu/<int:spu_id>/comments/', 
        views.fashionMallSPUCommentViewSet.as_view(), 
        name='spu-comments'
    ),
    *router.urls
]