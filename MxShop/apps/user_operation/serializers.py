from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
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


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(
        # 只读取 不提交
        read_only=True,
        format='%Y-%m-%d %H:%M'
    )

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(
        # 只读取 不提交
        read_only=True,
        format='%Y-%m-%d %H:%M'
    )
    signer_mobile = serializers.CharField(required=True, max_length=11, min_length=11,
                                          help_text="手机号码", label="手机号码",
                                          error_messages={
                                              "blank": "请输入手机号码",
                                              "required": "请输入手机号码",
                                              "max_length": "手机号码格式错误",
                                              "min_length": "手机号码格式错误",
                                          })

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name",
                  "signer_mobile", "add_time")
