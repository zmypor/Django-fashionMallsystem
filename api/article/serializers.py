from rest_framework import serializers

from apps.article.models import (
    fashionMallArticleCategory, fashionMallArticleContent
)


class fashionMallArticleCategorySerializer(serializers.ModelSerializer):
    """ 文章分类序列化 """
    class Meta:
        model = fashionMallArticleCategory
        fields = "__all__"
        
        
class fashionMallArticleContentSerializer(serializers.ModelSerializer):
    """ 文章内容序列化 """
    class Meta:
        model = fashionMallArticleContent
        fields = "__all__"
