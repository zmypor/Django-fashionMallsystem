from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.
from apps.common.models import BaseModelMixin


class fashionMallAddress(BaseModelMixin):
    """地址管理
    """
    name = models.CharField(_("名称"), max_length=50)
    parent = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        verbose_name=_("父级")
    )
    code = models.CharField(_("编码"), max_length=50)
    level = models.PositiveSmallIntegerField(_("级别"), default=1)

    class Meta:
        ordering = ["-add_date"]
        verbose_name = _("地址")
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.name


class fashionMallUserAddress(BaseModelMixin):
    """用户地址
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name=_("用户")
    )
    name = models.CharField(_("收货人"), max_length = 20)
    phone = models.CharField(_("手机号"), max_length = 11)
    code = models.CharField(_("邮政编码"), max_length = 6, blank=True, default="")
    detail = models.CharField(_("详细地址"), max_length = 150)
    is_default = models.BooleanField(_("默认地址"), default=False)

    class Meta:
        ordering = ["-add_date"]
        verbose_name = _("用户地址")
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.name