from .base import *

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 邮件控制台后端
# https://docs.djangoproject.com/zh-hans/5.0/topics/email/
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# 当开发模式时可以设置为True
CORS_ALLOW_ALL_ORIGINS = True

# 静态文件配置
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "dist",
]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# 支付宝配置
ALIPAY_APPID = '2021000122666025'
ALIPAY_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnGm4s+aI1LsCwL9i67GSqEICxqfkyzydk6TIA57M9++EHBUAsXHa5mpgUIQwlYKetzsdPnYK8rS7Pkn6RFogF639zoaRBIpCu8K/lazUB2PqykLdV+XH8DqtH3k6lz1hFRAOHDIn3wVqIUOC0H/G4TFsp8Cd/cgLYAFr12Fgm20/OW8GZNnhfZmmcbHc4el9CqWuEt1xRQLAgLiaDjTZ5RrgSwHem2p1kYKjcs0jw1M+IyKIZK0k6s/KwwqsSlG28ysP94nBI1v3vSIL0e25rvv5irYXi78hfmmO8+sBdYxBzkaF7tndTctTxTYMcnk/+1jKijahDW/72zTI0AwSxwIDAQAB'
ALIPAY_PRIVATE_KEY = 'MIIEowIBAAKCAQEAnIZvZfrK90k3KWK2G1mLxzaSSSWs6CO0oZrXiAMNr71La4hTHPDOBhrLOdUMX6tD1h2rzKhysRitkOe/vT0eI1bHQBs+9Z10aamrSFmOEdeisfLBqfjgjM2sXflzQwwbtGhRKoSoRDPHtC9NDFBm49EKEA3Nuyg8udUchlUzADBLrtV5delIC4AL+vocKJYFgxPqV6ZJpwQGgTry7Gn7NZIqOJ6RWItMuVj9n1sE50Pd/5H7dUhbOhct93E/X9HWU9DaAZofO/WJ7aRbrxKIccmDTiz8QYIp0LhQioKwFunuT+c5/Tbf8tXxZD5zpu+Gxlbg1wDNYXlpBNv0Y6q0NwIDAQABAoIBAEtaNLrFd3yAlLupt72G6FGpJdds+cZvmf/KiUQDJE2cNXi5Ejn2e1hZAcj/lYtg6bFka1aFKWG0XapKxvWVPLMKjbWA6FhZyrcrZTfZVRml078S/MSU+ZUPVpGPCzwV0iiRp7FuV4st2lAWDWOGOWInOk7sNkSJZGKaA7dvwLOvysLDLwb3c/82KP8HHDnB65ZSQrTNEzhYtJEpl6dnwLoRnnpBgW/J3H4X378ySgaw2nDlKrDvnZm+wE7UYNI0paBahRYfU67mZ9bER1zWJaKLlYu7GRoheWJdDLmOamF3YWqNR1uk95TsshduvJ8ALp7fFKKCycJfxwMQLETB5LECgYEA3DR9cNvKgS+Budlp64Hq5ezl9myhzzaaVvQfQX+pqgZL/fTSL80QLzwDtAwV8YSWf5UoGOkmETo3iKhM4g6cBKYgwpT5G8bdY5maTrz3FTdIKi5qyb8LNV2ufGM0cnbmhOOsFaxyrkOcea+7oHMCYs8XhWFHPa3an49fRuN2DsUCgYEAtff/1cIBWORAmFtuotuvUMniQY+4KCaK6eiuw0BjXGIyB34jj7xuTxEvdfNjo8avPfo/VoNqujkGyanqxgArviGvl8zsfhNuqAO9um62HgqCMPb88/Cd+K+uACz+EunSN4mt+TCM/fMnTMv0Plf2cTxqH2LnoYsR2ZU8a2Eo5ssCgYEAirpm7NsLUSfkynk2SbCnlAMTPZRivHDh+zYBGvqaoQsmhO/gG01NjPR6QMv8ZxPo3KfTgx4fZWsP4YBmL2SU1jjzGqNP7Tfz8fOrSz+xSiRxymFD1aYOIajLbIHzYMmXoNDucRkbhr4BrogP5J2QOz/MybLnduw4d52ToM1cayECgYBY4CTDOXtA+FKYV2flARlSgxgP32sZqSGF91CMKsGc2JUI1dH2nRjfY0xj9pk+34at5bDTx2H0THAFRQlW5bR3q6pAoSUMut78Dr+28+XdLFLEKY4Icwgk82Ev0snRYQR8fbFMGStzyTPzrVXAsWO7kL9gTwVFAFCajeoxpAW/GwKBgFi/KiL0RHz1S0a/mB4TP9i/j7kvN4xrdD6rPM8qpSgu6ywVzzSk6veUHDsqnCtqWUjCQ3XXUeKLw8JNS7CqQ3xJ0TmmdFoppf2oyewNV03sM8GrNgc5WIMdJxcAWtNaoiCMBNSMRJ1CekgfzjGbE32c1ZLxUEAs6jl667xKwTQV'
SANDBOX_DEBUG = True


from .drf import *
from .simple_jwt import *