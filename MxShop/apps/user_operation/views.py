from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer
from .models import UserFav, UserLeavingMessage
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 放到单独的view中就不会做全局的认证。
    # 如果放到settings中就会做全局的认证
    # 配置SessionAuthentication之后drf后台才可以登录
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 修改默认搜索字段
    lookup_field = "goods_id"

    # 然后需要重载这个方法。只返回当前用户的收藏信息
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        # 必须加这一行。以防出现意外的情况
        return UserFavSerializer


class LeavingMessageViewset(mixins.ListModelMixin, mixins.CreateModelMixin,
                     viewsets.GenericViewSet, mixins.DestroyModelMixin):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 放到单独的view中就不会做全局的认证。
    # 如果放到settings中就会做全局的认证
    # 配置SessionAuthentication之后drf后台才可以登录
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 返回当前用户的留言
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)
