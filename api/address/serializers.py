#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :serializers.py
@说明    :序列化器
@时间    :2024/04/22 16:01:18
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from rest_framework import serializers

from apps.address.models import fashionMallUserAddress, fashionMallAddress


class fashionMallUserAddressSerializer(serializers.ModelSerializer):
    """
    用户收货地址序列化器
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = fashionMallUserAddress
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data["user"]
        if validated_data["is_default"]:
            fashionMallUserAddress.objects.filter(user=user).update(is_default=False)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        user = validated_data["user"]
        if validated_data["is_default"]:
            fashionMallUserAddress.objects.filter(user=user).update(is_default=False)
        return super().update(instance, validated_data)
    
    
class fashionMallAddressSerializer(serializers.ModelSerializer):
    """
    地址序列化器
    """
    class Meta:
        model = fashionMallAddress
        fields = "__all__"