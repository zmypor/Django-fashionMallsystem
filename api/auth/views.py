from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import permissions

from api.common import pagination
from .serializers import (
    EmailSerializer, VerifyEmailCaptchaSerializer,
    RegisterSerializer, GroupSerializer, PermissionSerializer,
    UserSerializer
)


User = get_user_model()


def get_tokens_for_user(user):
    """ 手动获取令牌 """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'access_expire': refresh.access_token.payload['exp']   # token过期时间戳
    }
    
     
class SendCaptchaGenericAPIView(GenericAPIView):
    """ 发送验证码
    """
    serializer_class = EmailSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "发送成功！"})
    
    def perform_create(self, serializer):
        serializer.save()
        
        
class VerifyEmailCaptchaGenericAPIView(GenericAPIView):
    """验证邮箱
    """
    serializer_class = VerifyEmailCaptchaSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "校验通过！"})


class RegisterViewSet(mixins.CreateModelMixin, 
                      viewsets.GenericViewSet):
    """注册视图
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """用户视图
    """
    queryset = User.objects.order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, 
                          permissions.DjangoModelPermissions]
    pagination_class = pagination.PageNumberPagination
    filter_fields = ('username', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email', 'is_active', 'is_staff')


class PermissionViewSet(viewsets.ModelViewSet):
    """权限视图
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    pagination_class = pagination.PageNumberPagination
    filter_fields = ('name', 'codename', 'content_type__app_label', 'content_type__model')
    search_fields = ('name', 'codename')
    ordering_fields = ('name', 'codename', 'content_type__app_label', 'content_type__model')


class GroupViewSet(viewsets.ModelViewSet):
    """用户组视图
    """
    queryset = Group.objects.order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    pagination_class = pagination.PageNumberPagination
    filter_fields = ('name', )
    search_fields = ('name', )
    ordering_fields = ('name', )


class LogoutAPIView(APIView):
    """登出视图
    """
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "登出成功！"})
    

class UserInfoAPIView(APIView):
    """获取用户信息
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, many=False)
        return Response(serializer.data)