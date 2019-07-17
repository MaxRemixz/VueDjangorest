"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve

import xadmin
from MxShop.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name='goods_list')
# 配置category的url
router.register(r'categorys', CategoryViewset, base_name='categorys')

router.register(r'code', SmsCodeViewset, base_name='code')

router.register(r'users', UserViewset, base_name='users')

# 用户收藏
router.register(r"userfavs", UserFavViewset, base_name="userfavs")
# 用户留言
router.register(r"messages", LeavingMessageViewset, base_name="messages")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 商品列表页
    url(r'^', include(router.urls)),
    # 生成drf自动文档
    url(r'docs/', include_docs_urls(title='慕学生鲜')),
    # drf登录的配置
    url(r'^api-auth/', include('rest_framework.urls')),
    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),
]
