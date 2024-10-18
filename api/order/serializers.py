import random
from decimal import Decimal
from django.utils import timezone
from django.urls import reverse
from rest_framework import serializers

from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

from apps.order.models import fashionMallOrder, fashionMallOrderProduct
from api.shop.serializers import fashionMallSKUSerializer
from apps.alipay.config import client
from .utils import is_alipay


class fashionMallOrderProductSerializer(serializers.ModelSerializer):
    """ 
    订单商品序列化器
    """
    sku = fashionMallSKUSerializer(read_only=True, many=False)

    class Meta:
        model = fashionMallOrderProduct
        fields = "__all__"
        extra_kwargs = {
            "price": {
                "read_only": True
            },
            "order": {
                "read_only": True
            },
            "is_commented": {
                "read_only": True
            }
        }

class fashionMallOrderProductCreateSerializer(serializers.ModelSerializer):
    # 创建订单时序列化订单商品
    class Meta:
        model = fashionMallOrderProduct
        fields = "__all__"
        extra_kwargs = {
            "price": {
                "read_only": True
            },
            "order": {
                "read_only": True
            },
            "is_commented": {
                "read_only": True
            }
        }


class fashionMallOrderSerializer(serializers.ModelSerializer):
    """
    订单序列化器
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    fashionMallorderproduct_set = fashionMallOrderProductSerializer(many=True)

    class Meta:
        model = fashionMallOrder
        fields = "__all__"



class fashionMallOrderCreateSerializer(fashionMallOrderSerializer):
    """
    订单列表创建序列化器
    """
    fashionMallorderproduct_set = fashionMallOrderProductCreateSerializer(many=True)

    class Meta:
        model = fashionMallOrder
        fields = "__all__"
        extra_kwargs = {
            'order_number': {
                'read_only': True
            },
            'total_amount': {
                'read_only': True
            },
            'paid_amount': {
                'read_only': True
            },
            'pay_date': {
                'read_only': True
            },
            'freight': {
                'read_only': True
            },
            'shipping_method': {
                'read_only': True
            },
            'pay_method': {
                'read_only': True
            },
            'pay_status': {
                'read_only': True
            }
        }
    
    def create(self, validated_data):
        order_product_data = validated_data.pop('fashionMallorderproduct_set')
        order = fashionMallOrder.objects.create(**validated_data)
        for order_product in order_product_data:
            fashionMallOrderProduct.objects.create(
                order=order,
                price=order_product['sku'].price,
                **order_product
            )
        return order
    
    def validate(self, attrs):
        attrs['order_number'] = self.__order_number()
        attrs['total_amount'] = self.__total_amount(attrs['fashionMallorderproduct_set'])
        attrs['paid_amount'] = self.__paid_amount(attrs['fashionMallorderproduct_set'])
        return super().validate(attrs)
    
    def __order_number(self):
        return '{}{}{}'.format(
            timezone.now().strftime('%Y%m%d%H%M%S'),
            random.randint(1000, 9999),
            self.context['request'].user.id
        )
    
    def __total_amount(self, order_product_data) -> Decimal:
        # 商品总价
        total_amount = Decimal('0.00')
        for order_product in order_product_data:
            total_amount += order_product['sku'].price * order_product['num']
        return total_amount
    
    def __paid_amount(self, order_product_data) -> Decimal:
        # 实际支付
        return self.__total_amount(order_product_data)


class ByakeShopOrderPayMethodSerializer(serializers.ModelSerializer):
    """
    订单支付方式选择获取支付接口
    """

    pay_method = serializers.IntegerField(max_value=4, min_value=1)
    pay_url = serializers.URLField(read_only=True)
    
    # 支付
    class Meta:
        model = fashionMallOrder
        fields = ['pay_method', 'pay_url']

    def validate_pay_method(self, pay_method):
        if pay_method != 1:
            raise serializers.ValidationError("暂不支持该支付方式")
        return pay_method

    def update(self, instance, validated_data):
        if instance.pay_status in [0, 2, 3, 4, 5]:
            raise serializers.ValidationError("该订单状态下不允许支付！")
        # 支付前检查该订单是否已经支付过
        if validated_data['pay_method'] == 1 and (is_alipay(instance) is True):
            self.__update_pay_status(instance, 1)
            raise serializers.ValidationError("该订单已支付，无需重复支付！")
        instance.pay_url = self.get_pay_url(instance)
        return super().update(instance, validated_data)
    
    def __update_pay_status(self, obj, method:int):
        """
        更新订单支付状态
        """
        if obj.pay_status in [1]:
            obj.pay_status = 2
            obj.pay_method = method
            obj.pay_date = timezone.now()
            obj.save()

    def __get_alipay_api(self, obj) -> str:
        """
        获取支付宝支付接口
        """
        # 网页支付
        model = AlipayTradePagePayModel()
        model.out_trade_no = obj.order_number
        model.total_amount = str(obj.paid_amount)
        model.subject = obj.order_number
        model.body = "fashionMall订单支付"
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        alipay_api = AlipayTradePagePayRequest(biz_model=model)
        reverse_url = reverse("fashionMall_api:alipay-callback")
        alipay_api.return_url = self.get_callback_url(reverse_url)
        res = client.page_execute(alipay_api, http_method="GET")
        return res
    
    def get_callback_url(self, reverse_url):
        return f'{self.context["request"].scheme}://{self.context["request"].get_host()}{reverse_url}'

    def get_pay_url(self, obj):
        # 获取支付
        if self.validated_data.get('pay_method') == 1:
            return self.__get_alipay_api(obj)


class fashionMallOrderPayStatusSerializer(serializers.ModelSerializer):
    """
    订单支付状态
    """
    class Meta:
        model = fashionMallOrder
        fields = ['pay_status', 'order_number']
        extra_kwargs = {
            'order_number': {
                'read_only': True
            },
            'pay_status': {
                'read_only': True
            }
        }

    def update(self, instance, validated_data):
        validated_data['pay_status'] = 4
        return super().update(instance, validated_data)