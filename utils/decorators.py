from typing import Callable, Optional
import functools
from importlib import import_module

from django.views import View
from django.http.response import HttpResponse
from django.urls import URLPattern, URLResolver
from django.utils.functional import cached_property
from django.core.exceptions import ImproperlyConfigured

from apps.user.user_permissions.base_permissions import PermissionsError
from utils import restful
from apps.user.user_permissions import UserAction
from utils.types import Request


def permit(
        func_name: str,
        is_view: bool = False,
        field: Optional[str] = None,
) -> Callable:
    """
    限制视图函数被调用.
    field: 对指定参数的检验, 若存在, 则进行权限验证
    is_view: 是否把View视图类传递到权限类里获取相关参数进行权限验证
    """

    def inner(handler: Callable) -> Callable:
        """
        :param handler: 处理 HTTP 的视图函数; 类方法或函数均可
        :return: wrapper
        """

        def get_view(*args, **kwargs) -> View:
            for arg in args:
                if isinstance(arg, View):
                    return arg
            for _, arg in kwargs.items():
                if isinstance(arg, View):
                    return arg
            raise ValueError("'handler' must be a view function.")

        @functools.wraps(handler)
        def wrapper(*args, **kwargs) -> HttpResponse:
            view: View = get_view(View, *args, **kwargs)
            request: Request = view.request
            try:
                func = getattr(UserAction(request.user), func_name)
                if is_view and field:  # 针对某个字段并且需要传递view对象
                    func(view) if request.DATA.get(field) else None
                elif is_view:  # 仅需要传递view对象
                    func(view)
                elif field: # 仅需要针对某个字段
                    func() if request.DATA.get(field) else None
                else:
                    func()
            except PermissionsError as exception:
                return restful.forbidden(code=exception.code, message=exception.message)
            return handler(*args, **kwargs)
        return wrapper

    return inner


class DecoratedPatterns(object):
    """
    A wrapper for an urlconf that applies a decorator to all its views.
    """

    def __init__(self, urlconf_module, decorators):
        # ``urlconf_module`` may be:
        #   - an object with an ``urlpatterns`` attribute
        #   - an ``urlpatterns`` itself
        #   - the dotted Python path to a module with an ``urlpatters`` attribute
        self.urlconf = urlconf_module
        try:
            iter(decorators)
        except TypeError:
            decorators = [decorators]
        self.decorators = decorators

    def decorate_pattern(self, pattern):
        if isinstance(pattern, URLResolver):
            decorated = URLResolver(
                pattern.pattern,
                DecoratedPatterns(pattern.urlconf_module, self.decorators),
                pattern.default_kwargs,
                pattern.app_name,
                pattern.namespace,
            )
        else:
            callback = pattern.callback
            for decorator in reversed(self.decorators):
                callback = decorator(callback)
            decorated = URLPattern(
                pattern.pattern, callback, pattern.default_args, pattern.name,
            )
        return decorated

    @cached_property
    def urlpatterns(self):
        # urlconf_module might be a valid set of patterns, so we default to it.
        patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
        return [self.decorate_pattern(pattern) for pattern in patterns]

    @cached_property
    def urlconf_module(self):
        if isinstance(self.urlconf, str):
            return import_module(self.urlconf)
        else:
            return self.urlconf


def decorator_include(decorators, arg, namespace=None):
    """
    Works like ``django.conf.urls.include`` but takes a view decorator
    or an iterable of view decorators as the first argument and applies them,
    in reverse order, to all views in the included urlconf.
    """
    app_name = None
    if isinstance(arg, tuple):
        # callable returning a namespace hint
        try:
            urlconf, app_name = arg
        except ValueError:
            if namespace:
                raise ImproperlyConfigured(
                    "Cannot override the namespace for a dynamic module that provides a namespace"
                )
            # can happen for example when using decorator_include with ``admin.site.urls``
            urlconf, app_name, namespace = arg
    else:
        # No namespace hint - use manually provided namespace
        urlconf = arg

    decorated_urlconf = DecoratedPatterns(urlconf, decorators)
    namespace = namespace or app_name
    return (decorated_urlconf, app_name, namespace)


def login_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return restful.unauthorized(message="请先登录后再请求")
        else:
            return func(request, *args, **kwargs)
    return wrapper
