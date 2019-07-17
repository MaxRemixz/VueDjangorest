from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from random import choice
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from .models import VerifyCode

from utils.yunpian import YunPian
from MxShop.settings import APIKEY

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(APIKEY)
        # 正常是code = self.generate_code()
        code = "万事如意"
        sms_status = yun_pian.send_sms(code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # 由于setting中默认配置了BasicAuthentication所以访问会弹出登录框。
    # 改为支持在浏览器中添加session
    # 或者在header中添加token
    authentication_classes = (authentication.SessionAuthentication,
                              JSONWebTokenAuthentication)
    # permission_classes = (permissions.IsAuthenticated, )

    # 重载该方法可以动态根据请求来设置serializer类 来达到注册和获取信息的不同需求
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        # 必须加这一行。以防出现意外的情况
        return UserDetailSerializer

    # 重构该方法达到动态设置peimissions认证
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        # 必须加这一行。以防出现意外的情况
        return []

    # 重构该方法以达到注册登录并且使用Jwt生成token然后返回
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    # 重构该方法使得可以返回一个user对象给jwt_payload_handler方法调用
    def perform_create(self, serializer):
        return serializer.save()