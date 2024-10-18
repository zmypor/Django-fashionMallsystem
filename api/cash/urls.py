from django.urls import path
from . import views


urlpatterns = [
    path('cache/', views.fashionMallCacheSettlementAPIView.as_view(), name='cache'),
]
