#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :views.py
@说明    :购物车接口视图
@时间    :2024/04/09 18:00:56
@作者    :幸福关中&轻编程
@版本    :2.0
@微信    :baywanyun
'''

from rest_framework import viewsets, permissions

from api.cart.serializers import (
    fashionMallCartSerializer, fashionMallCartListSerializer
)
from api.common import pagination
from apps.cart.models import fashionMallCart


class fashionMallCartViewSet(viewsets.ModelViewSet):
    """
    购物车接口视图
    """
    queryset = fashionMallCart.objects.all()
    serializer_class = fashionMallCartSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        # 非管理员仅可查看自己的购物车数据
        if self.request.user.is_superuser is False:
            return queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return fashionMallCartListSerializer
        return super().get_serializer_class()

