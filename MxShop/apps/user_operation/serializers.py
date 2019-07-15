from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav


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
