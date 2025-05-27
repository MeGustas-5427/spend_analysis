from django.contrib.auth.models import AnonymousUser
from django.db.models import query, QuerySet

from apps.user.models import User
from apps.user.user_permissions.admin import AdminAction
from apps.user.user_permissions.employee import EmployeeAction
from apps.user.user_permissions.customer import CustomerAction
from apps.user.user_permissions.base_permissions import PermissionsError

from constants.code import Code


class UserActionMixin:
    def __init__(self, user: User):
        if isinstance(user, AnonymousUser):
            raise PermissionsError(Code.CLIENT_UNAUTHORIZED, Code.message(Code.CLIENT_UNAUTHORIZED))
        if user.level == User.LEVEL.管理员:
            self.action = AdminAction(user)
        elif user.level == User.LEVEL.员工:
            self.action = EmployeeAction(user)
        else:
            self.action = CustomerAction(user)


class UserSheetActionMixin(UserActionMixin):
    def get_user_sheet_queryset(self) -> QuerySet:
        """根据权限预设用户表查询列表范围"""
        return self.action.get_user_sheet_queryset()

    def has_permit_read_user(self, view) -> bool:
        """可否查询用户"""
        return self.action.has_permit_read_user(view)

    def has_permit_create_user(self):
        """可否创建用户"""
        return self.action.has_permit_create_user()

    def has_permit_edit_user(self):
        """可否编辑用户"""
        return self.action.has_permit_edit_user()

    def has_permit_del_user(self):
        """可否删除用户"""
        return self.action.has_permit_del_user()


class UserAction(
    UserSheetActionMixin,
):
    pass