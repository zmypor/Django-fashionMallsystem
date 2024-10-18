from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
from apps.common.models import BaseModelMixin


class fashionMallComment(BaseModelMixin):
    """评论"""

    class ScoreChoices(models.IntegerChoices):
        """评分"""
        ONE = 1, "1星"
        TWO = 2, "2星"
        THREE = 3, "3星"
        FOUR = 4, "4星"
        FIVE = 5, "5星"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="评论类型"
    )
    object_id = models.PositiveIntegerField(verbose_name="评论对象ID")
    content_object = GenericForeignKey("content_type", "object_id")
    content =models.TextField(verbose_name="评论内容")
    score = models.IntegerField(
        default=ScoreChoices.FIVE,
        choices=ScoreChoices.choices,
        verbose_name="评分"
    )
    status = models.BooleanField(
        default=True,
        verbose_name="状态"
    )

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ["-add_date"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
    
    def __str__(self) -> str:
        return self.content
