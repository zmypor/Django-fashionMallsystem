from django_filters import rest_framework as filters

from apps.common.models import fashionMallImagesAD


class fashionMallImagesADFilter(filters.FilterSet):
    """
    广告过滤
    """
    class Meta:
        model = fashionMallImagesAD
        fields = ['slug']