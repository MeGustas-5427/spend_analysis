from django.contrib import admin
from apps.materials.models import Category, Supplier, PurchaseRecord
# Register your models here.
# Django Admin 配置


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone']
    search_fields = ['name', 'contact_person']
    list_filter = ['name']


@admin.register(PurchaseRecord)
class PurchaseRecordAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'name', 'category', 'quantity', 'unit',
        'unit_price', 'total_amount', 'actual_paid', 'supplier'
    ]
    list_filter = ['date', 'category', 'supplier', 'unit']
    search_fields = ['name', 'specification', 'supplier__name']
    date_hierarchy = 'date'
    readonly_fields = ['total_amount', 'created_at', 'updated_at']

    fieldsets = (
        ('基本信息', {
            'fields': ('date', 'category', 'name', 'specification')
        }),
        ('数量和价格', {
            'fields': ('quantity', 'unit', 'unit_price', 'actual_paid', 'total_amount')
        }),
        ('供货商', {
            'fields': ('supplier',)
        }),
        ('其他信息', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # 编辑现有对象时
            return readonly
        return readonly