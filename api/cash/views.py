from django.core.cache import cache

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.shop.models import fashionMallSKU
from api.cart.serializers import fashionMallCartListSerializer
from api.shop.serializers import fashionMallSKUSerializer
from .serializers import fashionMallCacheSettlementSerializer


class fashionMallCacheSettlementAPIView(GenericAPIView):
    """
    缓存购物车结算
    """
    serializer_class = fashionMallCacheSettlementSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "ok"}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        """ 获取结算数据
        """
        cache_item = cache.get("settlement_%s" % request.user.id)
        if cache_item and cache_item.get("type") == "cart":
            cart_ids = cache_item.get("cart_ids")
            cart_list = request.user.fashionMallcart_set.filter(id__in=cart_ids)
            cart_list_serializer = fashionMallCartListSerializer(
                cart_list, many=True, context={"request": request}
            )
            return Response({"results": cart_list_serializer.data})
        
        elif cache_item and cache_item.get("type") == "sku":
            sku = fashionMallSKU.objects.get(id=cache_item.get("sku_id"))
            serializer = fashionMallSKUSerializer(
                sku, many=False, context={"request": request}
            )
            data = {}
            data["sku"] = serializer.data
            data["quantity"] = cache_item.get("sku_count")
            data["specs"] = list(sku.fashionMallskuspecs_set.values(
                "value__id", "value__value", "value__specs__name"
            ))
            return Response({"results": [data]})
        return Response({"msg": "未有结算数据"}, status=status.HTTP_204_NO_CONTENT)