#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :models.py
@说明    :商城相关模型
@时间    :2024/04/09 17:14:34
@作者    :幸福关中&轻编程
@版本    :2.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from apps.common.models import BaseModelMixin


class fashionMallCategory(BaseModelMixin):
    """Model definition for fashionMallCategory."""
    name = models.CharField(_("名称"), max_length=50)
    parent = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        verbose_name=_("父类"),
        blank=True,
        null=True
    )
    is_floor = models.BooleanField(_("是否为楼层"), default=False)
    sort = models.PositiveSmallIntegerField(_("排序"), default=0)

    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallCategory."""
        ordering = ['-sort']
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of fashionMallCategory."""
        return self.name


class fashionMallBrand(BaseModelMixin):
    """Model definition for fashionMallBrand."""
    name = models.CharField(_("名称"), max_length=50)
    logo = models.ImageField(_("logo"), upload_to="brand/%Y/%m", blank=True, null=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallBrand."""
        ordering = ['-add_date']
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        """Unicode representation of fashionMallBrand."""
        return self.name


class fashionMallSPU(BaseModelMixin):
    """Model definition for fashionMallSPU."""
    name = models.CharField(_("名称"), max_length=50)
    category = models.ForeignKey(
        fashionMallCategory, 
        on_delete=models.CASCADE, 
        verbose_name=_("分类")
    )
    brand = models.ForeignKey(
        fashionMallBrand, 
        on_delete=models.CASCADE,
        blank=True, 
        null=True, 
        verbose_name=_("品牌"),
    )
    detail = models.TextField(_("详情"), blank=True, null=True)
    is_sale = models.BooleanField(_("是否上架"), default=False)

    class Meta:
        """Meta definition for fashionMallSPU."""
        ordering = ['-add_date']
        verbose_name = _("商品")
        verbose_name_plural = verbose_name
    
    def __str__(self):
        """Unicode representation of fashionMallSPU."""
        return self.name
    

class fashionMallSpecs(BaseModelMixin):
    """Model definition for fashionMallSpecs."""
    name = models.CharField(_("名称"), max_length=50)
    
    class Meta:
        """Meta definition for fashionMallSpecs."""
        ordering = ['-add_date']
        verbose_name = _("规格")
        verbose_name_plural = verbose_name
    
    def __str__(self):
        """Unicode representation of fashionMallSpecs."""
        return self.name
    

class fashionMallSpecsValue(BaseModelMixin):
    """Model definition for fashionMallSpecsValue."""
    specs = models.ForeignKey(
        fashionMallSpecs, 
        on_delete=models.CASCADE, 
        verbose_name=_("规格")
    )
    value = models.CharField(_("值"), max_length=50)
    
    class Meta:
        """Meta definition for fashionMallSpecsValue."""
        ordering = ['-add_date']
        verbose_name = _("规格值")
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['specs', 'value'], 
                name='unique_specs_value'
            )
        ]
    
    def __str__(self):
        """Unicode representation of fashionMallSpecsValue."""
        return f"{self.specs.name}: {self.value}"


class fashionMallSKU(BaseModelMixin):
    """Model definition for fashionMallSKU."""
    spu = models.ForeignKey(
        fashionMallSPU, 
        on_delete=models.CASCADE, 
        verbose_name=_("SPU")
    )
    dash_price = models.DecimalField(_("划线价"), max_digits=10, decimal_places=2)
    price = models.DecimalField(_("价格"), max_digits=10, decimal_places=2)
    stock = models.IntegerField(_("库存"), default=0)
    sale = models.IntegerField(_("销量"), default=0)
    is_sale = models.BooleanField(_("是否上架"), default=False)
        
    class Meta:
        """Meta definition for fashionMallSKU."""
        ordering = ['-add_date']
        verbose_name = _("SKU")
        verbose_name_plural = verbose_name
    
    def __str__(self):
        """Unicode representation of fashionMallSKU."""
        return f"{self.spu.name} - {self.price}"
    

class fashionMallSKUSpecs(BaseModelMixin):
    """Model definition for fashionMallSKUSpecs."""
    sku = models.ForeignKey(
        fashionMallSKU, 
        on_delete=models.CASCADE, 
        verbose_name=_("SKU")
    )
    value = models.ManyToManyField(
        fashionMallSpecsValue,
        blank=True,
        verbose_name=_("值")
    )

    class Meta:
        """Meta definition for fashionMallSKUSpecs."""
        ordering = ['-add_date']
        verbose_name = _("SKU规格")
        verbose_name_plural = verbose_name
    
    def __str__(self):
        """Unicode representation of fashionMallSKUSpecs."""
        return f"{self.sku.spu.name}"
    

class fashionMallSPUImage(BaseModelMixin):
    """Model definition for fashionMallSPUImage."""
    spu = models.ForeignKey(
        fashionMallSPU, 
        on_delete=models.CASCADE, 
        verbose_name=_("SPU")
    )
    image = models.ImageField(_("图片"), upload_to="spu/%Y/%m", blank=True, null=True)
    status = models.BooleanField(_("是否显示"), default=False)

    class Meta:
        """Meta definition for fashionMallSPUImage."""
        ordering = ['-add_date']
        verbose_name = _("商品图")
        verbose_name_plural = verbose_name
    
    def __str__(self):
        """Unicode representation of fashionMallSPUImage."""
        return self.spu.name