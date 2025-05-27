import abc

from django.db.models import QuerySet

from apps.user.models import User
from utils.api_exception import ApiError


class PermissionsError(ApiError):
    pass


class BaseUserSheetPermissions:
    """用户表权限"""

    def get_user_sheet_queryset(self) -> QuerySet:
        """根据权限预设用户表查询列表范围"""
        raise NotImplementedError()

    def has_permit_read_user(self, view):
        """可否查询用户"""
        raise NotImplementedError()

    def has_permit_create_user(self):
        """可否创建用户"""
        raise NotImplementedError()

    def has_permit_edit_user(self):
        """可否编辑用户"""
        raise NotImplementedError()

    def has_permit_del_user(self):
        """可否删除用户"""
        raise NotImplementedError()


class PermissionsInitMixin(metaclass=abc.ABCMeta):
    def __init__(self, user: User) -> None:
        self._user = user