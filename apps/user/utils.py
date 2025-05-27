# accounts/utils.py  工具与鉴权

import jwt  # 用于生成和解码JWT
from django.http import JsonResponse  # 用于返回JSON响应
from django.conf import settings  # 访问settings配置
from datetime import datetime, timedelta, timezone  # 时间处理
from .models import User  # 引入User模型

def generate_jwt_token(user):
    """
    生成JWT Token
    :param user: 用户对象
    :return: 加密后的JWT Token
    """
    payload = {
        'user_id': user.id,  # 用户ID
        'exp': datetime.now(timezone.utc)+ timedelta(hours=settings.JWT_EXP_DELTA_HOURS),  # 过期时间
        'iat': datetime.now(timezone.utc)  # 签发时间
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_jwt_token(token):
    """
    解码JWT Token
    :param token: JWT Token字符串
    :return: payload字典或None
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token过期
    except jwt.InvalidTokenError:
        return None  # Token无效

def login_required(view_func):
    """
    装饰器：确保请求者已登录
    :param view_func: 视图函数
    :return: 包装后的视图函数
    """
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')  # 获取Authorization头
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'detail': 'Unauthorized'}, status=401)  # 未授权
        token = auth_header.split(' ')[1]  # 获取Token
        payload = decode_jwt_token(token)  # 解码Token
        if not payload:
            return JsonResponse({'detail': 'Token is invalid or expired'}, status=401)  # Token无效或过期
        try:
            user = User.objects.get(id=payload['user_id'])  # 获取用户对象
        except User.DoesNotExist:
            return JsonResponse({'detail': 'User not found'}, status=401)  # 用户不存在
        request.user = user  # 将用户对象附加到请求
        return view_func(request, *args, **kwargs)  # 调用原视图函数
    return wrapper

def admin_required(view_func):
    """
    装饰器：确保请求者具有管理员权限
    :param view_func: 视图函数
    :return: 包装后的视图函数
    """
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user.is_admin_flag:
            return JsonResponse({'detail': 'Forbidden'}, status=403)  # 禁止访问
        return view_func(request, *args, **kwargs)  # 调用原视图函数
    return wrapper
