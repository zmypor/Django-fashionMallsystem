from django_filters import rest_framework as filters

from apps.order.models import fashionMallOrder

class fashionMallOrderFilter(filters.FilterSet):
    
    class Meta:
        model = fashionMallOrder
        fields = ['pay_method', 'pay_status',]
