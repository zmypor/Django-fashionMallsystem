from django_filters import rest_framework as filters

from apps.shop.models import (
    fashionMallCategory, fashionMallSPU
)


class fashionMallCategoryFilter(filters.FilterSet):
    """ 商品分类过滤器  """
    class Meta:
        model = fashionMallCategory
        fields = ['parent',]


class fashionMallSPUFilter(filters.FilterSet):
    """ 商品过滤器  """
    class Meta:
        model = fashionMallSPU
        fields = ['category', 'brand',]

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            category = fashionMallCategory.objects.filter(
                id=category_id, parent__isnull=True
            )
            if category.exists():
                sub_cates = category.first().fashionMallcategory_set.values_list(
                    'id', flat=True
                )
                queryset = fashionMallSPU.objects.filter(
                    category__id__in=list(sub_cates)
                )
                from .utils import spu_alias_annotate
                return spu_alias_annotate(queryset)
        return super().filter_queryset(queryset)

