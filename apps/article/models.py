from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
# Create your models here.
from apps.common.models import BaseModelMixin


class fashionMallArticleCategory(BaseModelMixin):
    """Model definition for fashionMallArticleCategory."""
    name = models.CharField(_("名称"), max_length=50)
    parent = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        verbose_name=_("父类"),
        blank=True,
        null=True
    )
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallArticleCategory."""
        ordering = ['-add_date']
        verbose_name = 'fashionMallArticleCategory'
        verbose_name_plural = 'fashionMallArticleCategorys'

    def __str__(self):
        """Unicode representation of fashionMallArticleCategory."""
        return self.name


class fashionMallArticleContent(BaseModelMixin):
    """Model definition for fashionMallArticleContent."""
    title = models.CharField(_("标题"), max_length=100)
    desc = models.CharField(_("描述"), max_length=150, blank=True, default="")
    keywords = models.CharField(_("关键词"), max_length=150, blank=True, default="")
    category = models.ForeignKey(
        fashionMallArticleCategory, 
        on_delete=models.CASCADE, 
        verbose_name=_("分类")
    )
    content = models.TextField(verbose_name=_("内容"))
    status = models.BooleanField(default=True, verbose_name=_("状态"))
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for fashionMallArticleContent."""
        ordering = ['-add_date']
        verbose_name = 'fashionMallArticleContent'
        verbose_name_plural = 'fashionMallArticleContents'

    def __str__(self):
        """Unicode representation of fashionMallArticleContent."""
        return self.title

    def save(self, *args, **kwargs):
        from django.utils.html import strip_tags
        if not self.desc:
            self.desc = strip_tags(self.content)[:140]
        super().save(*args, **kwargs)
        
    @cached_property
    def next_article(self):
        # 下一篇
        try:
            return self.get_next_by_add_date()
        except fashionMallArticleContent.DoesNotExist:
            return fashionMallArticleContent.objects.last()
    
    @cached_property
    def previous_article(self):
        # 上一篇
        try:
            return self.get_previous_by_add_date()
        except fashionMallArticleContent.DoesNotExist:
            return fashionMallArticleContent.objects.first()