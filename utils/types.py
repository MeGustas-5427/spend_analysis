from typing import Any, Dict, Union, Callable

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.contrib.auth.models import AnonymousUser

from apps.user.models import User

__all__ = ["Request"]


class Request(WSGIRequest):
    user: Union[User, AnonymousUser]
    DATA: Dict[str, Any]


HTTPHandler = Callable[..., HttpResponse]
