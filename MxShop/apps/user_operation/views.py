from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import UserFavSerializer
from .models import UserFav
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    用户收藏功能
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    # 放到单独的view中就不会做全局的认证。
    # 如果放到settings中就会做全局的认证
    # 配置SessionAuthentication之后drf后台才可以登录
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 然后需要重载这个方法。只返回当前用户的收藏信息
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
