from .serializers import GoodsSerializer, CategorySerializer
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework import viewsets

from .models import Goods, GoodsCategory
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter)
    filterset_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewset(mixins.ListModelMixin,
                      viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin):
    """
    List:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
