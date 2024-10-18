from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.
from apps.common.models import BaseModelMixin
from apps.shop.models import fashionMallSKU


class fashionMallCart(BaseModelMixin):
    """
    购物车
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name=_("用户")
    )
    sku = models.ForeignKey(
        fashionMallSKU, 
        on_delete=models.CASCADE,
        verbose_name=_("SKU")
    )
    quantity = models.PositiveSmallIntegerField(_("数量"), default=1)

    class Meta:
        ordering = ["-add_date"]
        verbose_name = _("购物车")
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=["user", "sku"], 
                name="unique_user_sku"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.sku}"