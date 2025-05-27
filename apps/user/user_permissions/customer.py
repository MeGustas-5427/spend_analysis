from django.db.models import QuerySet

from apps.user.models import User
from apps.user.user_permissions.base_permissions import (
    BaseUserSheetPermissions,
    PermissionsInitMixin,
    PermissionsError
)

from constants.code import Code


class UserSheetPermissionsMixin(BaseUserSheetPermissions, PermissionsInitMixin):
    """用户表权限"""
    def get_user_sheet_queryset(self) -> QuerySet:
        """根据权限预设用户表查询列表范围"""
        return User.objects.filter(pk=self._user.id)

    def has_permit_read_user(self, view):
        """可否查询用户"""
        if self._user.id == view.kwargs["pk"]:
            return True
        raise PermissionsError(Code.无权查询用户, Code.message(Code.无权查询用户))

    def has_permit_create_user(self):
        """可否创建用户"""
        raise PermissionsError(Code.无权创建用户, Code.message(Code.无权创建用户))

    def has_permit_edit_user(self):
        """可否编辑用户"""
        raise PermissionsError(Code.无权编辑用户, Code.message(Code.无权编辑用户))

    def has_permit_del_user(self):
        """可否删除用户"""
        raise PermissionsError(Code.无权删除用户, Code.message(Code.无权删除用户))


class CustomerAction(
    UserSheetPermissionsMixin,
):
    pass