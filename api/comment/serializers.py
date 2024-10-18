from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.comment.models import fashionMallComment
from apps.order.models import fashionMallOrderProduct
from apps.shop.models import fashionMallSPU

class fashionMallCommentSerializer(serializers.ModelSerializer):
    """ 评论序列化器 """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = fashionMallComment
        fields = "__all__"


class fashionMallCommentOrderProductSerializer(fashionMallCommentSerializer):
    """ 订单商品评论列表序列化器 """

    content_type = serializers.HiddenField(
        default=ContentType.objects.get_for_model(fashionMallOrderProduct),
        help_text="评论类型",
        required=False
    )
    def create(self, validated_data):
        try:
            orderproduct = fashionMallOrderProduct.objects.get(
                id=validated_data["object_id"]
            )
            # 订单状态修改
            order = orderproduct.order
            
            # 判断是否已经评价过
            if orderproduct.is_commented:
                raise serializers.ValidationError("该商品已评论")
            # 判断是否为自己的订单
            if order.user != self.context["request"].user:
                raise serializers.ValidationError("该订单不是你的订单, 不能评价")
            # 评价状态修改
            orderproduct.is_commented = True
            orderproduct.save()
            # 判断订单商品未评价的商品是否全部评价
            is_commented_orderproducts = fashionMallOrderProduct.objects.filter(
                order=order, is_commented=False
            ).exists()
            # 修改订单状态
            if not is_commented_orderproducts:
                order.pay_status = 5
                order.save()
        except fashionMallOrderProduct.DoesNotExist:
            raise serializers.ValidationError("订单商品不存在")
        return super().create(validated_data)


class fashionMallSPUCommentsSerializer(serializers.Serializer):

    spu_id = serializers.IntegerField(
        min_value=1,
        label="商品ID",
        help_text="商品ID",
        error_messages={
            "min_value": "商品ID必须大于0",
            "required": "商品ID不能为空",
        },
    )

    def validate(self, attrs):
        spu_id = attrs.get("spu_id")
        try:
            self.get_spu(spu_id)
        except fashionMallSPU.DoesNotExist:
            raise serializers.ValidationError("商品不存在")
        return attrs
    
    def get_spu(self, spu_id):
        return fashionMallSPU.objects.get(id=spu_id)