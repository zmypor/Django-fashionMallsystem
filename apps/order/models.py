from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.
from apps.common.models import BaseModelMixin
from apps.shop.models import fashionMallSKU


class fashionMallOrder(BaseModelMixin):
    """Model definition for fashionMallOrder."""
    class PayMethod(models.IntegerChoices):
        ALIPAY = 1, _('支付宝支付')
        WXPAY = 2, _('微信支付')
        SURPLUS = 3, _('余额支付')
        COLLECT = 4, _('货到付款')

    class PayStatus(models.IntegerChoices):
        EXPIRED = 0, _('已过期')
        UNPAID = 1, _('待支付')
        UNSHIPPED = 2, _('待发货')
        UNRECEIVED = 3, _('待收货')
        UNRATED = 4, _('待评价')
        DONE = 5, _('已完成')

    class ShippingMethod(models.IntegerChoices):
        SHIPPING_EXPRESS = 1, _("快递")
        SELF_PICKUP = 2, _("自提")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name=_("用户")
    )
    pay_method = models.PositiveSmallIntegerField(
        choices=PayMethod.choices,
        default=PayMethod.ALIPAY,
        verbose_name="支付方式"
    )
    pay_status = models.PositiveSmallIntegerField(
        choices=PayStatus.choices,
        default=PayStatus.UNPAID,
        verbose_name="订单状态"
    )
    order_number = models.CharField('订单编号', max_length=50, unique=True)
    total_amount = models.DecimalField('商品总价', max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField('实际支付', max_digits=10, decimal_places=2)
    pay_date = models.DateTimeField('支付时间', null=True, blank=True)
    address = models.CharField('收货地址', max_length=150)
    pick_up = models.CharField('收件人', max_length=50)
    phone = models.CharField('手机', max_length=11)
    email = models.EmailField('邮箱', max_length=254, blank=True, default='')
    shipping_method = models.PositiveSmallIntegerField(
        '配送方式', 
        choices=ShippingMethod.choices,
        default=ShippingMethod.SHIPPING_EXPRESS
    )
    freight = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00')  
    )
    mark = models.TextField('备注', blank=True, default='')

    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallOrder."""
        ordering = ['-add_date']
        verbose_name = '订单管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of fashionMallOrder."""
        return self.order_number


class fashionMallOrderProduct(BaseModelMixin):
    """Model definition for fashionMallOrderProduct."""
    order = models.ForeignKey(
        fashionMallOrder, 
        on_delete=models.CASCADE, 
        verbose_name="订单"
    )
    price = models.DecimalField("单价", max_digits=10, decimal_places=2)
    num = models.PositiveSmallIntegerField("数量", default=1)
    specs = models.JSONField(blank=True, default=list, verbose_name="规格")
    sku = models.ForeignKey(
        fashionMallSKU,
        on_delete=models.PROTECT,
        verbose_name="商品"
    )
    is_commented = models.BooleanField(
        default=False,
        verbose_name="是否评价"
    )

    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallOrderProduct."""
        ordering = ['-add_date']
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of fashionMallOrderProduct."""
        specs = [
            f"{spec['value__specs__name']}:{spec['value__value']}" 
            for spec in self.specs
        ]
        return f"{self.sku.spu.name}/{self.price}x{self.num}/{specs}"
