import json
import typing
import zoneinfo
from typing import Optional, Any
from datetime import date, time, datetime

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Prefetch, QuerySet
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views import View
from django.http import JsonResponse, RawPostDataException
from django.forms import model_to_dict
from django.conf import settings

from apps.user.user_permissions import UserAction
from apps.user.utils import generate_jwt_token
from apps.user.models import User
from constants.code import Code
from utils import restful
from utils.api_exception import ApiError
from utils.decorators import permit
from utils.types import Request
from utils.views import FilterApiView


# Create your views here.
class UserRegisterView(View):
    def post(self, request):
        """注册账号"""
        data = json.loads(request.body)
        phone: Optional[str] = data.get('phone')
        password: Optional[str] = data.get('password') or "Qwert654321"
        user = User(phone=phone, password=make_password(password))
        try:
            user.full_clean()
        except ValidationError as e:
            if Code.message(Code.用户已存在) in e.messages:
                raise ApiError(code=Code.用户已存在, message=Code.message(Code.用户已存在))
            raise ApiError(code=Code.手机号格式不正确, message=Code.message(Code.手机号格式不正确))

        user.save()
        return restful.created(token=generate_jwt_token(user), id=user.id)


class UserLoginView(View):
    def post(self, request):
        """登录"""
        data = json.loads(request.body)
        phone: Optional[str] = data.get('phone')
        password: Optional[str] = data.get('password')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise ApiError(code=Code.用户或密码错误, message=Code.message(Code.用户或密码错误))

        if not user.check_password(password):
            raise ApiError(code=Code.用户或密码错误, message=Code.message(Code.用户或密码错误))

        return restful.ok(result={**model_to_dict(user, exclude=["password"]), 'token': generate_jwt_token(user)})



class UserListView(FilterApiView):

    def __init__(self, **kwargs: typing.Any):
        super().__init__()
        self.exclude = None
        self.user = None

    def dispatch(self, request: Request, *args, **kwargs):
        self.user: User = request.user
        self.exclude = ['password']
        return super().dispatch(request, *args, **kwargs)

    @permit('get_user_sheet_queryset')
    def get(self, request):
        """
            后续要分页显示
            获取用户列表，需要设置权限，普通员工可以获取客户列表，
            管理员可以获取客户列表、普通员工列表
        """
        return self.list(request)

    def serialization(self, object_list) -> list:
        return [model_to_dict(user, exclude=self.exclude) for user in object_list]

    def get_init_queryset(self):
        return UserAction(self.user).get_user_sheet_queryset()
