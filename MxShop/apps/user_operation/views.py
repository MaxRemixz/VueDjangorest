from rest_framework import viewsets
from rest_framework import mixins
from .serializers import UserFavSerializer
from .models import UserFav


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    用户收藏功能
    """
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
