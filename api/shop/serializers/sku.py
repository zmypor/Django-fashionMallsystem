from rest_framework import serializers
from apps.shop.models import fashionMallSKU


class fashionMallSKUSerializer(serializers.ModelSerializer):

    title = serializers.CharField(source="spu.name", read_only=True)
    img = serializers.ImageField(source="spu.fashionMallspuimage_set.first.image", read_only=True)

    class Meta:
        model = fashionMallSKU
        fields = '__all__'