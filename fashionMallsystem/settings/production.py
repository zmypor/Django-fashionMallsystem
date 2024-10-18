from .base import *

# 静态文件配置
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "dist",
]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# 允许跨域访问的站点列表
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]

# 邮件后端配置
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# 缓存配置
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}

# 支付宝配置
ALIPAY_APPID = ''
ALIPAY_PUBLIC_KEY = ''
ALIPAY_PRIVATE_KEY = ''
SANDBOX_DEBUG = False

from .drf import *
from .simple_jwt import *