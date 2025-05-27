import typing
import datetime
import random
import string
import uuid

import pytz
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Page
from django.shortcuts import _get_queryset
from django.core.handlers.wsgi import WSGIRequest

def get_uuid4():
    return str(uuid.uuid4()).replace("-", "")


def get_order_no() -> str:
    """根据当前系统时间来生成订单号。时间精确到微秒"""
    return timezone.localtime().strftime("%Y%m%d%H%M%S%f")


def random_str(num: int) -> str:
    """生成随机字符串"""
    return "".join(random.sample(string.ascii_letters + string.digits, num))


def filter_dict(
    data: dict, namelist: typing.Iterable[str], notfound_error: bool = False
) -> dict:
    """
    从字典中摘取需要的部分

    如果 notfound_error 为真, 则在 namelist 中存在 data 中没有的 key 时, 会抛出一个 KeyError 异常
    """
    newdict = {}

    for name in namelist:
        try:
            newdict[name] = data[name]
        except KeyError as e:
            if notfound_error:
                raise e
    return newdict


def pagination(
    request, queryset: Page, page: int, count: int, orders_count: int, params=""
):
    """API接口分页参数"""
    _pagination = {"count": orders_count}
    url = request.build_absolute_uri().split("?")[0]
    if queryset.has_next():
        _pagination["next"] = f"{url}?p={page+1}&page_size={count}&{params}"
    else:
        _pagination["next"] = queryset.has_next()

    if queryset.has_previous():
        _pagination["previous"] = f"{url}?p={page-1}&page_size={count}&{params}"
    else:
        _pagination["previous"] = queryset.has_previous()

    return _pagination


def convert_timezone(time_in: datetime.datetime) -> datetime.datetime:
    """
    用来将系统自动生成的datetime格式的utc时区时间转化为本地时间
    :param time_in: datetime.datetime格式的utc时间
    :return:输出仍旧是datetime.datetime格式，但已经转换为本地时间
    """
    time_utc = time_in.replace(tzinfo=pytz.timezone("UTC"))
    time_local = time_utc.astimezone(pytz.timezone(settings.TIME_ZONE))
    return time_local


def get_object_or_None(klass, *args, **kwargs):
    """
    pypi: https://pypi.org/project/django-annoying/
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
