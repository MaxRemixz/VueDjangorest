from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart
from goods.serializers import GoodsSerializer


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


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
    # 这里的gooods是外键关系
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # 继承serializers.Serializer的话就必须重写create方法去验证
    # 因为create会对数据进行验证。而我们在model中添加了unique_together唯一性。如果直接
    # 使用会报错。所以需要重载create方法
    def create(self, validated_data):
        # 根据情况创建或更新商品购物车数量
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

    def update(self, instance, validated_data):
        """
        修改商品数量
        :param instance:
        :param validated_data:
        :return:
        """
        instance.nums = validated_data['nums']
        instance.save()
        return instance
