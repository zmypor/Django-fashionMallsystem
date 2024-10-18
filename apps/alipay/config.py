#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :config.py
@说明    :支付宝配置
@时间    :2024/03/29 14:46:43
@作者    :幸福关中&轻编程
@版本    :2.0
@微信    :baywanyun
'''

import logging
from django.conf import settings
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient


APPID = settings.ALIPAY_APPID
ALIPAY_PUBLIC_KEY = settings.ALIPAY_PUBLIC_KEY
APP_PRIVATE_KEY = settings.ALIPAY_PRIVATE_KEY
SANDBOX_DEBUG = settings.SANDBOX_DEBUG

if SANDBOX_DEBUG:
    SERVE_URL = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
else:
    SERVE_URL = 'https://openapi.alipaydev.com/gateway.do'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger(__name__)


class AlipayConfig:
    """
    支付宝配置
    """
    def __init__(self, default_config=None, client=None) -> None:
        self.default_config = default_config or AlipayClientConfig
        self.client = client or DefaultAlipayClient
        self.extra_config = {}

    def get_client(self, **kwargs):
        """
        获取支付宝客户端
        """
        config = self.default_config(sandbox_debug=kwargs.get('sandbox_debug', True))
        all_config = {**kwargs, **self.extra_config}
        try:
            config_dict = {
                key: value 
                for key, value in all_config.items() 
                if hasattr(config, key)
            }
            dynamic_keys = {
                key: value 
                for key, value in all_config.items() 
                if not hasattr(config, key)
            }
            # 设置已知的配置属性
            for key, value in config_dict.items():
                setattr(config, key, value)
            # 如果存在动态配置，记录错误并处理
            if dynamic_keys:
                logging.error(f"以下配置项不存在: {', '.join(dynamic_keys.keys())}")
        except AttributeError as e:
            logging.error(f"设置配置项时出错: {e}")
        return self.client(config, logger=logger)


config = AlipayConfig()

client = config.get_client(
    app_id=APPID,
    app_private_key=APP_PRIVATE_KEY,
    alipay_public_key=ALIPAY_PUBLIC_KEY,
    sign_type="RSA2",
    server_url=SERVE_URL
)