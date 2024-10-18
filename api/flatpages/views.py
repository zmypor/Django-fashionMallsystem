#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :views.py
@说明    :单页接口
@时间    :2024/04/22 16:02:06
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
from django.http import HttpResponsePermanentRedirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions

from django.contrib.flatpages.models import FlatPage

from api.common import pagination
from .serializers import FlatPageSerializer


class BaseFlatPageView:
    """
    基础视图
    """
    serializer_class = FlatPageSerializer
    def flatpage(self, request, url):
        if not url.startswith("/"):
            url = "/" + url
        site_id = get_current_site(request).id
        try:
            f = get_object_or_404(FlatPage, url=url, sites=site_id)
        except Http404:
            if not url.endswith("/") and settings.APPEND_SLASH:
                url += "/"
                f = get_object_or_404(FlatPage, url=url, sites=site_id)
                return HttpResponsePermanentRedirect("%s/" % request.path)
            else:
                raise
        return f
    
    def render_flatpage(self, request, f):
        if f.registration_required and not request.user.is_authenticated:
            return Response(
                {"detail": "This page is only available to logged in users."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(f, many=False)
        return Response(serializer.data)
    
    def get_serializer(self, *args, **kwargs):
        return FlatPageSerializer(*args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.flatpage(request, url=kwargs.get("url"))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class FlatPageAPIView(BaseFlatPageView, APIView):
    """
    获取flatpage详情
    """
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    
    def get_queryset(self):
        return FlatPage.objects.all()

    def get(self, request, *args, **kwargs):
        f = self.flatpage(request, url=kwargs.get("url"))
        return self.render_flatpage(request, f)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ 删除 """
        f = self.flatpage(request, url=kwargs.get("url"))
        f.delete()
        return Response(
            {"detail": "Method \"DELETE\" not allowed."}, 
            status=status.HTTP_200_OK
        )



class FlatPageViewSet(mixins.ListModelMixin, 
                      mixins.CreateModelMixin, 
                      viewsets.GenericViewSet):
    """ 单页列表及新增

    Args:
        mixins (_type_): _description_
        mixins (_type_): _description_
        viewsets (_type_): _description_
    """
    serializer_class = FlatPageSerializer
    queryset = FlatPage.objects.all()
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = pagination.PageNumberPagination
