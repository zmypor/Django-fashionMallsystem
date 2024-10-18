#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :urls.py
@说明    :权限相关url
@时间    :2024/03/29 10:25:23
@作者    :幸福关中&轻编程
@版本    :2.0
@微信    :baywanyun
'''

from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenVerifyView, TokenRefreshView
)
from .import views


router = DefaultRouter()

router.register("users", views.UserViewSet, basename="users")
router.register("groups", views.GroupViewSet, basename="groups")
router.register("permissions", views.PermissionViewSet, basename="permissions")


urlpatterns = [
    # 获取token post
    path("token/", TokenObtainPairView.as_view(), name="token"),
    # 刷新token post
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    # 验证token post 
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    # 获取用户信息【当前登录用户信息】
    path("userinfo/", views.UserInfoAPIView.as_view(), name="userinfo"),
    # 发送验证码
    path("sendemailcaptcha/", 
        views.SendCaptchaGenericAPIView.as_view(), 
        name="send-email-captcha"),
    # 验证邮箱
    path("verifyemailcaptcha/", 
        views.VerifyEmailCaptchaGenericAPIView.as_view(), 
        name="verify-email-captcha"),
    # 注册用户
    path("register/", 
        views.RegisterViewSet.as_view({"post": "create"}), 
        name="register"),
    # 退出登录
    path("logout/", 
        views.LogoutAPIView.as_view(), 
        name="logout"),

    *router.urls
]


 