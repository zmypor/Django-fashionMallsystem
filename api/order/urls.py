from django.urls import path

from .alipay_callback import AlipayCallbackView
from . import views

urlpatterns = [
    path(
        'orders/', 
        views.fashionMallOrderListCreateAPIView.as_view(), 
        name='ordersAPI'
    ),
    path(
        '<str:order_number>/paymethod/', 
        views.ByakeShopOrderPayMethodAPIView.as_view(), 
        name='paymethodAPI'
    ),
    path(
        '<str:order_number>/detail/', 
        views.fashionMallOrderRetrieveDestroyAPIView.as_view(), 
        name='detailAPI'
    ),
    path(
        '<str:order_number>/paystatus/', 
        views.fashionMallOrderPayStatusUpdateAPIView.as_view(), 
        name='paystatusAPI'
    ),
    path(
        'alipay-callback/', 
        AlipayCallbackView.as_view(),
        name='alipay-callback'
    ),
]
