from django.core.cache import cache
from rest_framework import serializers
from apps.shop.models import fashionMallSKU

class fashionMallCacheSettlementSerializer(serializers.Serializer):
    """
    结算缓存序列化器
    """
    cart_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        min_length=1,
        max_length=50,
        allow_empty=False,
        required=False
    )
    sku_id = serializers.IntegerField(min_value=1, required=False)
    sku_count = serializers.IntegerField(min_value=1, required=False)
    type = serializers.ChoiceField(choices=["cart", "sku"], required=True)

    def validate(self, attrs):
        if attrs.get("type") == "cart":
            if not attrs.get("cart_ids"):
                raise serializers.ValidationError("cart_ids不能为空")
        elif attrs.get("type") == "sku": 
            if not attrs.get("sku_id"):
                raise serializers.ValidationError("sku_id不能为空")
            else:
                if not fashionMallSKU.objects.filter(id=attrs.get("sku_id")).exists():
                    raise serializers.ValidationError("sku_id不存在")
            if not attrs.get("sku_count"):
                raise serializers.ValidationError("sku_count不能为空")
        return super().validate(attrs)

    def create(self, validated_data):
        cache.set(
            "settlement_%s" % self.context['request'].user.id,
            validated_data,
            timeout=60*60*24
        )
        return validated_data