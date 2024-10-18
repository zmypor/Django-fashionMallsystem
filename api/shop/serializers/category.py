from rest_framework import serializers
from apps.shop.models import fashionMallCategory


class fashionMallCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = fashionMallCategory
        fields = '__all__'