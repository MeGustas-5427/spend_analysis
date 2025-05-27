import json
import traceback

from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin

# from apps.user.user_permissions.base_permissions import PermissionsError
from utils import restful
from utils.api_exception import ApiError


class RequestParsingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.JSON = None
        if (
            request.content_type == "application/octet-stream"
            and int(request.META.get("CONTENT_LENGTH", "0")) > 0
        ):
            return HttpResponseBadRequest(
                "Get content-type: application/octet-stream,"
                + " you must change content-type."
            )

        if request.content_type != "application/json":
            if request.method not in ("GET", "POST"):
                # if you want to know why do that,
                # read https://abersheeran.com/articles/Django-Parse-non-POST-Request/
                if hasattr(request, "_post"):
                    del request._post
                    del request._files

                _shadow = request.method
                request.method = "POST"
                request._load_post_and_files()
                request.method = _shadow
            request.DATA = request.POST
        else:
            try:
                request.JSON = json.loads(request.body)
                request.DATA = request.JSON
            except ValueError as ve:
                return HttpResponseBadRequest(
                    "Unable to parse JSON data. Error: {0}".format(ve)
                )


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        """https://zhuanlan.zhihu.com/p/55594369"""
        # traceback.print_exc()  # 打印报错
        exception_class = exception.__class__


        # if exception_class == PermissionsError:
        #     return restful.forbidden(exception.code, message=exception.message)
        if exception_class == ApiError:
            return restful.bad_request(exception.code, message=exception.message)
        raise exception
