from django.contrib.auth.base_user import AbstractBaseUser
from django.core import validators
from django.db import models
from django.utils import timezone

from constants.code import Code
from utils import ChoiceEnum
from utils.models import ModelUpdateMixin

# Create your models here.

phone_regex = validators.RegexValidator(
    regex=r'1[3456789]\d{9}',
    message=Code.message(Code.手机号格式不正确)
)

phone_length_validator = validators.MaxLengthValidator(
    limit_value=11,
    message=Code.message(Code.手机号格式不正确)
)

name_length_validator = validators.MaxLengthValidator(
    limit_value=10,
    message=Code.message(Code.名字过长)
)

class User(AbstractBaseUser, ModelUpdateMixin):
    name = models.CharField("用户姓名", max_length=10,
                            null=True, blank=True,
                            validators=[name_length_validator]
                            )  # 针对多号用户，可以重复
    phone = models.CharField("手机号码", max_length=11,
                             unique=True,
                             null=False,
                             blank=False,
                             validators=[phone_regex, phone_length_validator],
                             error_messages={
                                 "unique": Code.message(Code.用户已存在),
                             },
                             )
    class LEVEL(ChoiceEnum):
        用户 = 0
        员工 = 1
        管理员 = 2

    level = models.PositiveSmallIntegerField("级别", choices=LEVEL, default=LEVEL.用户)
    created_at = models.DateTimeField("注册时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    # 设置用户名字段和必填字段
    USERNAME_FIELD = 'phone'  # 使用phone作为登录字段
    REQUIRED_FIELDS = ['name', 'phone', 'password']  # 创建超级用户时需要填写的字段

    class Meta:
        verbose_name = "用户基本信息"
        verbose_name_plural = verbose_name

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=["last_login"])
