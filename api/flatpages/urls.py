from django.urls import path
from . import views


urlpatterns = [
    path("detail/<path:url>", views.FlatPageAPIView.as_view(), name="flatpage_url"),
    path("list/", views.FlatPageViewSet.as_view({"get": "list"}), name="flatpage_list"),
    path("create/", views.FlatPageViewSet.as_view({"post": "create"}), name="flatpage_create"),
]