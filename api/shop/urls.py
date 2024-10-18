from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('category', views.fashionMallCategoryViewSet, basename='category')
router.register('spu', views.fashionMallSPUViewSet, basename='spu')
router.register('sku', views.fashionMallSKUViewSet, basename='sku')
router.register('sku-specs', views.fashionMallSKUSpecsViewSet, basename='sku-specs')
router.register('specs', views.fashionMallSpecsViewSet, basename='specs')
router.register('specs-value', views.fashionMallSpecsValueViewSet, basename='specs-value')
router.register('brand', views.fashionMallBrandViewSet, basename='brand')
router.register('spu-image', views.fashionMallSPUImageViewSet, basename='spu-image')


urlpatterns = [
    *router.urls
]