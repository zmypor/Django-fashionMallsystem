from rest_framework import serializers
from apps.shop.models import fashionMallSpecsValue


class fashionMallSpecsValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = fashionMallSpecsValue
        fields = '__all__'