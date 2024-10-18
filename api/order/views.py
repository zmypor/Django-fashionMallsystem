#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :views.py
@说明    :订单相关
@时间    :2024/04/22 16:01:48
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from rest_framework import generics, permissions

from api.common import pagination
from apps.order.models import fashionMallOrder
from .serializers import (
    fashionMallOrderSerializer, fashionMallOrderCreateSerializer, 
    ByakeShopOrderPayMethodSerializer, fashionMallOrderPayStatusSerializer
)
from .filters import fashionMallOrderFilter


class fashionMallOrderListCreateAPIView(generics.ListCreateAPIView):

    """
    订单列表
    """
    queryset = fashionMallOrder.objects.all()
    serializer_class = fashionMallOrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    filterset_class = fashionMallOrderFilter

    def get_queryset(self):
        """
        过滤订单
        """
        return super().get_queryset().filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return fashionMallOrderSerializer
        return super().get_serializer_class()
    

class ByakeShopOrderPayMethodAPIView(generics.UpdateAPIView):
    """
    选择支付方式，获取支付地址
    """
    serializer_class = ByakeShopOrderPayMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'order_number'
    lookup_url_kwarg = 'order_number'
    queryset = fashionMallOrder.objects.all()

    def get_queryset(self):
        """过滤订单"""
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

class fashionMallOrderRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """订单详情
    """
    lookup_field = 'order_number'
    lookup_url_kwarg = 'order_number'
    queryset = fashionMallOrder.objects.all()
    serializer_class = fashionMallOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """过滤订单"""
        return super().get_queryset().filter(user=self.request.user)


class fashionMallOrderPayStatusUpdateAPIView(generics.UpdateAPIView):
    """
    订单支付状态
    """
    serializer_class = fashionMallOrderPayStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = fashionMallOrder.objects.all()
    lookup_field = 'order_number'
    lookup_url_kwarg = 'order_number'

    def get_queryset(self):
        """过滤订单"""
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    