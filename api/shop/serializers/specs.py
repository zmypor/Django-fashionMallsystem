from rest_framework import serializers
from apps.shop.models import fashionMallSpecs


class fashionMallSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = fashionMallSpecs
        fields = '__all__'