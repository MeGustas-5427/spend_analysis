from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from apps.user.models import User
from apps.user.utils import decode_jwt_token


class ParsingJWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get("HTTP_TOKEN", None) \
                or request.COOKIES.get("token", None)  # js的websocket无法设置headers
        if token:
            jwt_data = decode_jwt_token(token)
        else:
            jwt_data = None

        if jwt_data:
            try:
                user = User.objects.get(pk=jwt_data["user_id"])
                # 解析出有效用户则设置
                setattr(request, "user", user)
            except ObjectDoesNotExist:
                pass

        if getattr(request, "user", None) is None:
            # 在这之前没有判断出身份则设为匿名用户
            setattr(request, "user", AnonymousUser())
