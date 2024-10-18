from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class BaseModelMixin(models.Model):
    """ 全局模型基类 """
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    is_delete = models.BooleanField(
        default=False, 
        editable=False, 
        verbose_name="删除标记"
    )
    
    # TODO

    class Meta:
        abstract = True

    
class fashionMallImagesAD(BaseModelMixin):
    """ 广告图片 """
    name = models.CharField(_("名称"), max_length=50)
    image = models.ImageField(_("图片"), upload_to="images/ad/%Y/%m/%d/")
    url = models.URLField(_("链接"), max_length=200, blank=True, null=True)
    slug = models.SlugField(
        _("Slug"), 
        max_length=50,
        default="home-banner", 
        blank=True,
        help_text="slug可以重复，用作广告位标识，如：banner-1"
    )
    sort = models.IntegerField(_("排序"), default=0)

    class Meta:
        verbose_name = _("图片广告")
        verbose_name_plural = _("图片广告")
        ordering = ["-sort"]

    def __str__(self) -> str:
        return self.name