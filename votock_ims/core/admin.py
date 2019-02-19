from django.contrib import admin
from .models import Product, Supplier, PurchaseOrder, PurchaseOrderLine, SaleOrderLine, SaleOrder, Purchaser

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Purchaser)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'inventory_in_box', 'inventory_in_total', )


class PurchaseOrderLineInline(admin.TabularInline):
    model = PurchaseOrderLine
    verbose_name = "采购产品行"
    min_num = 1
    extra = 0


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('purchase_date', 'supplier', )
    inlines = (PurchaseOrderLineInline, )


class SaleOrderLineInline(admin.TabularInline):
    model = SaleOrderLine
    verbose_name = "销售产品行"
    min_num = 1
    extra = 0


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ('sale_date', 'purchaser', )
    inlines = (SaleOrderLineInline, )
