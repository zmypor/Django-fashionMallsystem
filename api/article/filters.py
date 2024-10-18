from django_filters import rest_framework as filters

from apps.article.models import fashionMallArticleContent


class fashionMallArticleContentFilter(filters.FilterSet):
    """
    文章内容过滤器
    """
    add_date__year = filters.NumberFilter(
        field_name="add_date__year", 
        lookup_expr='exact', 
        label="年"
    )
    add_date__month = filters.NumberFilter(
        field_name="add_date__month", 
        lookup_expr='exact', 
        label="月"
    )

    class Meta:
        model = fashionMallArticleContent
        fields = ['category', 'add_date__year', 'add_date__month']
