#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :views.py
@说明    :地址视图接口
@时间    :2024/04/22 15:50:14
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from rest_framework import viewsets
from rest_framework import permissions

from apps.address.models import (
    fashionMallAddress, fashionMallUserAddress
)
from .serializers import (
    fashionMallAddressSerializer, fashionMallUserAddressSerializer
)


class fashionMallAddressViewSet(viewsets.ModelViewSet):
    """Address Administration Interface
    """
    queryset = fashionMallAddress.objects.all()
    serializer_class = fashionMallAddressSerializer
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly
    ]


class fashionMallUserAddressViewSet(viewsets.ModelViewSet):
    """User Address Administration Interface
    """
    queryset = fashionMallUserAddress.objects.all()
    serializer_class = fashionMallUserAddressSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)