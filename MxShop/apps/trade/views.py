from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer
from utils.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart,OrderInfo, OrderGoods


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能开发
    list：
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    # 修改前端传过来的数据为商品的id。这样更好的操作数据的增删
    lookup_field = "goods_id"
    # queryset = ShoppingCart.objects.all()

    # 重写列表页的显示  这样就返回当前用户的购物车记录
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    # 重构get_serializer_class以达到动态设置serializer
    # 可以满足不同的页面需求
    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer


class OrderViewset(viewsets.GenericViewSet, mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.DestroyModelMixin):
    """
    订单管理
    list:
        获取个人订单
    create:
        新增订单
    delete:
        删除订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order
