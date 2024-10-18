from rest_framework import serializers
from apps.shop.models import fashionMallSPUImage


class fashionMallSPUImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = fashionMallSPUImage
        fields = '__all__'