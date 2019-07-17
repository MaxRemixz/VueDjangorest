from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # 一般做收藏的话。最好能返回收藏数据的id。便于删除
        model = UserFav
        # 设置字段为联合唯一索引
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏",
            )
        ]
        fields = ("user", "goods", "id")
