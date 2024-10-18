#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :views.py
@说明    :公共视图
@时间    :2024/04/17 13:40:28
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from rest_framework import viewsets, permissions

from apps.common.models import fashionMallImagesAD
from .serializers import fashionMallImagesADSerializer
from .filters import fashionMallImagesADFilter


class fashionMallImagesADViewSet(viewsets.ModelViewSet):
    """
    广告位
    """
    queryset = fashionMallImagesAD.objects.all()
    serializer_class = fashionMallImagesADSerializer
    filterset_class = fashionMallImagesADFilter
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()