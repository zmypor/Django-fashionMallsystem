from django.db.models import F
from django.db.utils import IntegrityError
from rest_framework import serializers

from api.shop.serializers import fashionMallSKUSerializer
from apps.cart.models import fashionMallCart


class fashionMallCartSerializer(serializers.ModelSerializer):
    """
    购物车序列化器
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = fashionMallCart
        fields = "__all__"
        extra_kwargs = {
            'quantity': {'required': True},
            'sku': {'required': True}
        }
        validators = []

    def validate(self, attrs):
        try:
            if attrs["quantity"] > attrs["sku"].stock:
                raise serializers.ValidationError("库存不足")
        except KeyError:
            raise serializers.ValidationError("参数错误,quantity与sku不能为空")
        return super().validate(attrs)
    
    def validate_sku(self, sku):
        if sku.is_delete:
            raise serializers.ValidationError("商品已删除")
        elif not sku.is_sale:
            raise serializers.ValidationError("商品已下架")
        return sku

    def validate_quantity(self, quantity):
        if quantity <= 0:
            raise serializers.ValidationError("数量必须大于0")
        return quantity

    def create(self, validated_data):
        try:
            obj = fashionMallCart.objects.create(**validated_data)
        except IntegrityError:
            carts = fashionMallCart.objects.filter(
                user=validated_data["user"],
                sku=validated_data["sku"]
            )
            carts.update(quantity=F("quantity") + validated_data["quantity"])
            obj = carts.first()
        return obj


class fashionMallCartListSerializer(serializers.ModelSerializer):
    """
    购物车列表序列化器
    """
    sku = fashionMallSKUSerializer(many=False, read_only=True)
    specs = serializers.SerializerMethodField()

    class Meta:
        model = fashionMallCart
        fields = "__all__"

    def get_specs(self, obj):
        """
        获取规格
        """
        specs = obj.sku.fashionMallskuspecs_set.values(
            "value__specs__name", "value__id", "value__value"
        )
        return list(specs)