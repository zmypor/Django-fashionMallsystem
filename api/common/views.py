#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
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
