from rest_framework import serializers
from apps.shop.models import fashionMallSKUSpecs


class fashionMallSKUSpecsSerializer(serializers.ModelSerializer):

    class Meta:
        model = fashionMallSKUSpecs
        fields = '__all__'