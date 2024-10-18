from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from apps.comment.models import fashionMallComment
from apps.order.models import fashionMallOrderProduct
from .serializers import (
    fashionMallCommentOrderProductSerializer, 
    fashionMallSPUCommentsSerializer
)


class fashionMallCommentViewSet(viewsets.ModelViewSet):
    """
    评论
    """
    queryset = fashionMallComment.objects.filter(is_delete=False)
    serializer_class = fashionMallCommentOrderProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        重写queryset，只返回当前用户评论
        """
        return super().get_queryset().filter(user=self.request.user)


class fashionMallSPUCommentViewSet(generics.GenericAPIView):
    """
    SPU评论
    """
    serializer_class = fashionMallSPUCommentsSerializer
    lookup_url_kwarg = 'spu_id'

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**kwargs})
        serializer.is_valid(raise_exception=True)
        spu = serializer.get_spu(spu_id=kwargs.get('spu_id'))
        comments = self.get_comments(spu)
        data = {
            "avg_score": self.get_avg_score(comments),
            "score_rating": self.get_score_rating(comments),
            "comments": self.get_comments_data(comments),
            "count": self.get_comments_count(comments),
        }
        return Response(data)
    
    def get_comments(self, spu):
        content_type = ContentType.objects.get_for_model(fashionMallOrderProduct)
        ids = fashionMallOrderProduct.objects.filter(sku__spu=spu).values_list("id", flat=True)
        return fashionMallComment.objects.filter(
            content_type=content_type, object_id__in=list(ids)
        )
    
    def get_avg_score(self, comments):
        # 平均分数
        from django.db.models import Avg
        return comments.aggregate(
            avg_score=Avg("score", distinct=True)
        ).get("avg_score") or 0
    
    def get_comments_data(self, comments):
        # 评论列表
        return list(comments.values(
            "id", "user__username", "content", "score", "add_date"
        ))
    
    def get_comments_count(self, comments):
        # 评论数量
        return comments.count()
    
    def get_score_rating(self, comments):
        # 好评率
        count = self.get_comments_count(comments) or 1
        rating = comments.filter(
            score__gte=fashionMallComment.ScoreChoices.THREE
        ).count() / count * 100
        return rating 
    