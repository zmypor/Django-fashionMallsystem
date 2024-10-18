from rest_framework import serializers
from apps.shop.models import fashionMallBrand


class fashionMallBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = fashionMallBrand
        fields = '__all__'