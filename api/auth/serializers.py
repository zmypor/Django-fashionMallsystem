#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :serializers.py
@说明    :权限相关序列化
@时间    :2024/03/29 10:26:12
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer
)
from apps.cart.models import fashionMallCart


User = get_user_model()
CODE_LENGTH = 4

class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):  
    """ 登录获取令牌 """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        cart_count = fashionMallCart.objects.filter(user=self.user).aggregate(
            cart_count=models.Sum('quantity'))['cart_count'] or 0
        data['user'] = UserSerializer(self.user).data
        data['user']['cart_count'] = cart_count
        return data


class EmailSerializer(serializers.Serializer):
    """邮箱
    """
    email = serializers.EmailField(
        label="邮箱", 
        max_length=150,
        min_length=3
    )
    
    def save(self, **kwargs):
        """
        保存并发送验证码到指定邮箱。
        
        从utils模块导入code_random函数，生成指定长度的验证码，
        并通过邮件将验证码发送到验证数据中的邮箱地址。
        
        参数:
        - **kwargs: 可变关键字参数，用于传递额外的参数。
        
        返回值:
        - captcha: 发送到邮箱的验证码。
        """
        from utils import code_random
        # 生成验证码
        code = code_random(code_length=CODE_LENGTH)
        # 从验证数据中获取邮箱地址
        email = self.validated_data['email']
        # 使用cache.get_or_set方法设置或获取邮箱对应的验证码，并设置过期时间为300秒
        captcha = cache.get_or_set(email, code, 300)
        try:
            # 尝试发送邮件，包含验证码内容
            send_mail(
                "fashionMall邮箱验证码，请查收！",
                f"您的验证码为：{captcha}，5分钟内有效.",
                settings.DEFAULT_FORM_EMAIL,
                [email],
                fail_silently=False,
            )
        except BadHeaderError:
            # 如果邮件头出错，则抛出验证错误
            raise serializers.ValidationError("Invalid header found.")
        return captcha
    
    
class VerifyEmailCaptchaSerializer(serializers.Serializer):
    """校验邮箱验证码
    """
    email = serializers.EmailField(
        label="邮箱", 
        max_length=150,
        min_length=3
    )
    code = serializers.CharField(
        label="验证码",
        max_length=CODE_LENGTH,
        min_length=3,
        write_only=True
    )
    
    def validate(self, attrs):
        """
        对传入的属性进行验证。
        
        首先调用父类的validate方法处理属性，然后尝试从缓存中获取通过email对应的验证码，并与传入的code进行比较。
        如果两者不匹配，抛出验证错误；如果email或code不存在，同样抛出验证错误。
        
        :param attrs: 包含验证信息的字典，预期包含email和code两个键。
        :return: 验证通过后返回处理后的属性字典。
        """
        
        # 调用父类的validate方法处理属性
        attrs = super().validate(attrs)
        try:
            # 检查缓存中的验证码与传入的验证码是否匹配
            if cache.get(attrs['email']) != attrs['code']:
                raise serializers.ValidationError("验证码错误，校验失败！")
        except KeyError:
            # 如果email或code不存在，抛出验证错误
            raise serializers.ValidationError("还未发送验证码，请先获取验证码！")
        return attrs


class RegisterSerializer(VerifyEmailCaptchaSerializer, serializers.ModelSerializer):
    """
    用户注册序列化器
    需要通过验证码验证邮箱的合法性
    """
    
    class Meta:
        model = User  # 指定序列化器使用的模型
        fields = ("username", "password", "email", "code")  # 定义序列化器需要处理的字段
        extra_kwargs = {
            'password': {'write_only': True},  # 密码字段只用于写入
            'code': {'write_only': True},  # 验证码字段只用于写入
        }

    def validate_email(self, email):
        """
        验证邮箱的唯一性
        参数:
            email (str): 用户提交的邮箱地址
        返回值:
            str: 验证通过返回邮箱地址
        异常:
            serializers.ValidationError: 如果邮箱已被注册，抛出异常
        """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("该邮箱已被注册，请更换邮箱！")
        return email

    def validate_password(self, password):  
        """
        自定义密码验证方法，将密码加密处理
        参数:
            password (str): 用户提交的明文密码
        返回值:
            str: 加密后的密码
        """
        return make_password(password)
    
    def validate(self, attrs):
        """
        在序列化器的默认验证流程之后，删除'code'字段，准备数据进行进一步处理
        参数:
            attrs (dict): 包含所有字段及其值的字典
        返回值:
            dict: 验证并处理后的字段及其值的字典
        """
        super().validate(attrs)  # 调用父类的验证方法
        del attrs['code']  # 删除验证码字段，因为验证码在验证过程中使用后不再需要
        return attrs


class PermissionSerializer(serializers.ModelSerializer):
    """
    权限序列化器
    """
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """
    用户组序列化器
    """
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    """
    groups = GroupSerializer(many=True, read_only=True)
    user_permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('first_name', 'last_name',)

    def validate_password(self, password):
        return make_password(password)