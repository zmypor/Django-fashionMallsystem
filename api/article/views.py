from rest_framework import viewsets
from rest_framework import permissions

from apps.article import models
from api.common import pagination
from .filters import fashionMallArticleContentFilter
from . import serializers


class fashionMallArticleCategoryViewSet(viewsets.ModelViewSet):
    """文章分类
    """
    queryset = models.fashionMallArticleCategory.objects.all()
    serializer_class = serializers.fashionMallArticleCategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class fashionMallArticleContentViewSet(viewsets.ModelViewSet):
    """文章内容
    """
    queryset = models.fashionMallArticleContent.objects.filter(status=True)
    serializer_class = serializers.fashionMallArticleContentSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = pagination.PageNumberPagination
    filterset_class = fashionMallArticleContentFilter
    search_fields = ['title', 'content', 'category__name', ]
    ordering_fields = ['add_date', 'pub_date', ]