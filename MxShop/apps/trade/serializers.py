from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label="数量",
                                    error_messages={
                                        "min_value": "商品数量不能小于1",
                                        "required": "请选择购买数量",
                                    })
    # 由于这里继承的是serializers.Serializer.不是继承自serializers.ModelSerializer
    # 所以需要指明query_set
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # 继承serializers.Serializer的话就必须重写create方法去验证
    # 因为serializers.Serializer相当于是form表单。不是像modelform一样会直接验证保存
    def create(self, validated_data):
        # 在serializer中.request并没有直接放在self中。只有在view中才可以直接用self取到reuqest
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed
