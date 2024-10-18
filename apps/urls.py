from django.urls import path, include, re_path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)
from apps.common.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('drf/', include('rest_framework.urls')),
    path('api/', include('api.urls', namespace='fashionMall_api')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), 
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]