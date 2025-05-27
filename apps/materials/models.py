from django.db import models
from decimal import Decimal

from utils.models import ModelUpdateMixin


class Category(models.Model, ModelUpdateMixin):
    """商品类别"""
    name = models.CharField(max_length=50, verbose_name="类别名称", unique=True)
    description = models.TextField(blank=True, verbose_name="类别描述")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = "商品类别"

    def __str__(self):
        return self.name


class Supplier(models.Model, ModelUpdateMixin):
    """供货商"""
    name = models.CharField(max_length=100, verbose_name="供货商名称", unique=True)
    contact_person = models.CharField(max_length=50, blank=True, verbose_name="联系人")
    phone = models.CharField(max_length=20, blank=True, verbose_name="联系电话")
    address = models.TextField(blank=True, verbose_name="地址")

    class Meta:
        verbose_name = "供货商"
        verbose_name_plural = "供货商"

    def __str__(self):
        return self.name


class PurchaseRecord(models.Model, ModelUpdateMixin):
    """采购记录"""
    date = models.DateField(verbose_name="日期")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="类别"
    )
    name = models.CharField(max_length=100, verbose_name="名称")
    specification = models.CharField(max_length=100, blank=True, verbose_name="规格")
    unit = models.CharField(max_length=20, verbose_name="单位")
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="数量"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="单价"
    )
    actual_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="实付"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name="供货商"
    )

    # 自动计算字段
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="应付金额",
        editable=False,
        default=Decimal('0.00')
    )

    # 可选的备注字段
    notes = models.TextField(blank=True, verbose_name="备注")

    # 创建和更新时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "采购记录"
        verbose_name_plural = "采购记录"
        ordering = ['-date', '-created_at']  # 按日期倒序排列

    def save(self, *args, **kwargs):
        # 自动计算应付金额（数量 × 单价）
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.name} ({self.supplier.name})"
