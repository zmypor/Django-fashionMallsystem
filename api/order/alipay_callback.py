from django.conf import settings
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.order.models import fashionMallOrder


class AlipayCallbackView(APIView):
    """
    支付宝回调
    """
    def get(self, request, *args, **kwargs):
        data = request.GET.dict()
        order_number = data.get("out_trade_no")
        if not order_number:
            return Response({"message": "订单不存在"})
        order_qs = fashionMallOrder.objects.filter(order_number=order_number)
        is_verify = self.verify_sign(data)
        if is_verify:
            from decimal import Decimal
            from django.utils import timezone
            order_qs.update(
                pay_status=2, pay_date=timezone.now(),
                paid_amount=Decimal(data.get("total_amount")),
                pay_method=1
            )
        if settings.ALIPAY_RETURN_URL:
            return redirect(f"{settings.ALIPAY_RETURN_URL}/pay/{order_number}")
        return Response({"message": "ok"})
    
    def post(self, request, *args, **kwargs):
        """
        支付宝回调
        """
        data = request.POST.dict()
        order_number = data.get("out_trade_no")
        if not order_number:
            return Response({"message": "订单不存在"})
        order_qs = fashionMallOrder.objects.filter(order_number=order_number)
        is_verify = self.verify_sign(data)
        if is_verify:
            from decimal import Decimal
            from django.utils import timezone
            order_qs.update(
                pay_status=2, pay_date=timezone.now(),
                paid_amount=Decimal(data.get("total_amount")),
                pay_method=1
            )
        return Response("success")
    
    def verify_sign(self, data):
        # 除去 sign、sign_type 两个参数
        is_verify = False
        sign = data.pop('sign')
        sign_type = data.pop('sign_type')
        # 将剩下参数进行 url_decode，然后进行字典排序，组成字符串，得到待签名字符串    
        message = '&'.join([
            f"{k}={v}" 
            for k, v in dict(sorted(data.items(), key=lambda d: d[0], reverse=False)).items()
        ]).encode("utf-8")
        # 4. 验签
        from alipay.aop.api.util.SignatureUtils import verify_with_rsa
        from apps.alipay.config import ALIPAY_PUBLIC_KEY
        is_verify = verify_with_rsa(
            public_key=ALIPAY_PUBLIC_KEY,
            message=message,
            sign=sign,
        )
        return is_verify

