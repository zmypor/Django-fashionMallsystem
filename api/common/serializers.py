from rest_framework import serializers

from apps.common.models import fashionMallImagesAD


class fashionMallImagesADSerializer(serializers.ModelSerializer):
    """
    广告序列化
    """
    class Meta:
        model = fashionMallImagesAD
        fields = "__all__"