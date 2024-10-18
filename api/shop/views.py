from rest_framework import viewsets
from rest_framework import permissions

from api.common import pagination
from apps.shop.models import (
    fashionMallSPU,
    fashionMallCategory,
    fashionMallSKUSpecs,
    fashionMallSPUImage,
    fashionMallSpecsValue,
    fashionMallSpecs,
    fashionMallSKU,
    fashionMallBrand,
)
from api.shop.serializers import (
    fashionMallSPUSerializer,
    fashionMallCategorySerializer,
    fashionMallSKUSpecsSerializer,
    fashionMallSPUImageSerializer,
    fashionMallSpecsValueSerializer,
    fashionMallSpecsSerializer,
    fashionMallSKUSerializer,
    fashionMallBrandSerializer,
    fashionMallSPUDetailSerializer,
)
from .filters import (
    fashionMallCategoryFilter,
    fashionMallSPUFilter
)


class fashionMallCategoryViewSet(viewsets.ModelViewSet):
    """
    商品分类
    """
    queryset = fashionMallCategory.objects.all()
    serializer_class = fashionMallCategorySerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filterset_class = fashionMallCategoryFilter
    search_fields = ["name", "parent__name",]
    ordering_fields = ["add_date", "pub_date",]


class fashionMallSPUViewSet(viewsets.ModelViewSet):
    """
    商品SPU
    """
    queryset = fashionMallSPU.objects.filter(is_sale=True)
    serializer_class = fashionMallSPUSerializer
    pagination_class = pagination.PageNumberPagination
    filterset_class = fashionMallSPUFilter
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filter_fields = ["name", "category", "brand",]
    search_fields = ["name", "category__name", "brand__name",]
    ordering_fields = ["price", "sale", "add_date", "pub_date",]

    def get_queryset(self):
        queryset = super().get_queryset()
        from .utils import spu_alias_annotate
        return spu_alias_annotate(queryset)
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return fashionMallSPUDetailSerializer
        return fashionMallSPUSerializer


class fashionMallSKUSpecsViewSet(viewsets.ModelViewSet):
    """
    商品SKU规格
    """
    queryset = fashionMallSKUSpecs.objects.all()
    serializer_class = fashionMallSKUSpecsSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    # filter_fields = ["sku", "value",]
    search_fields = ["value__value",]
    ordering_fields = ["add_date", "pub_date",]


class fashionMallSPUImageViewSet(viewsets.ModelViewSet):
    """
    商品SPU图片
    """
    queryset = fashionMallSPUImage.objects.all()
    serializer_class = fashionMallSPUImageSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
   # filter_fields = []
    search_fields = ["spu__name",]
    ordering_fields = ["add_date", "pub_date",]


class fashionMallSpecsValueViewSet(viewsets.ModelViewSet):
    """
    商品规格值
    """
    queryset = fashionMallSpecsValue.objects.all()
    serializer_class = fashionMallSpecsValueSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filter_fields = ["specs", "value",]
    search_fields = ["specs__name", "value",]
    ordering_fields = ["add_date", "pub_date",]


class fashionMallSpecsViewSet(viewsets.ModelViewSet):
    """
    商品规格
    """
    queryset = fashionMallSpecs.objects.all()
    serializer_class = fashionMallSpecsSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filter_fields =["name",]
    search_fields = ["name",]
    ordering_fields = ["add_date", "pub_date",]


class fashionMallSKUViewSet(viewsets.ModelViewSet):
    """
    商品SKU
    """
    queryset = fashionMallSKU.objects.all()
    serializer_class = fashionMallSKUSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filter_fields = ["spu", "price", "stock", "sale", "is_sale",]
    search_fields = ["spu__name",]
    ordering_fields = ["add_date", "pub_date",]


class fashionMallBrandViewSet(viewsets.ModelViewSet):
    """
    商品品牌
    """
    queryset = fashionMallBrand.objects.all()
    serializer_class = fashionMallBrandSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filter_fields =["name", "logo",]
    search_fields = ["name",]
    ordering_fields = ["add_date", "pub_date",]
