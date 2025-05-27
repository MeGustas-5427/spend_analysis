from django.db.models import QuerySet

from apps.user.models import User
from apps.user.user_permissions.base_permissions import (
    BaseUserSheetPermissions,
    BaseRoomPermissions,
    BaseBookingPermissions,
    PermissionsInitMixin,
    PermissionsError
)

from constants.code import Code


class UserSheetPermissionsMixin(BaseUserSheetPermissions, PermissionsInitMixin):
    """用户表权限"""
    def get_user_sheet_queryset(self):
        """根据权限预设用户表查询列表范围"""
        return User.objects

    def has_permit_read_user(self, view):
        """可否查询用户"""
        return True

    def has_permit_create_user(self):
        return True

    def has_permit_edit_user(self):
        """可否编辑用户"""
        return True

    def has_permit_del_user(self):
        """可否删除用户"""
        return True





class AdminAction(
    UserSheetPermissionsMixin,
):
    pass