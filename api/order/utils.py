import json

from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from apps.alipay.config import client

def is_alipay(obj):
    """
    判断支付宝订单是否支付成功
    :param obj: fashionMallOrderModel对象
    :return: True-支付成功, False-支付失败
    """
    flag = False  # 默认支付失败标志
    biz_content = AlipayTradeQueryModel()  # 创建AlipayTradeQueryModel对象
    biz_content.out_trade_no = obj.order_number  # 设置商户订单号
    request = AlipayTradeQueryRequest()  # 创建AlipayTradeQueryRequest对象
    request.biz_content = biz_content  # 设置请求参数
    res = json.loads(client.execute(request))  # 发起请求并得到响应结果
    try:
        flag = bool(res["trade_status"] == "TRADE_SUCCESS")  # 判断订单是否支付成功
    except KeyError:
        flag = False  # 出现KeyError异常，表示订单查询失败
    return flag