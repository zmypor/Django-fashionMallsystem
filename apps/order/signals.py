from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.cart.models import fashionMallCart
from apps.order.models import fashionMallOrderProduct


@receiver(post_save, sender=fashionMallOrderProduct)
def order_product_post_save(sender, instance, **kwargs):
    """
    订单保存后，更新订单状态
    """
    sku = instance.sku
    sku.stock -= instance.num
    sku.sale += instance.num
    sku.save()
    
    settlement = cache.get('settlement_%s' % instance.order.user.id)
    if settlement and settlement.get('cart_ids'):
        fashionMallCart.objects.filter(id__in=settlement.get('cart_ids')).delete()
    # 清理缓存
    cache.delete('settlement_%s' % instance.order.user.id)
