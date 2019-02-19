
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Product, Supplier, PurchaseOrder, PurchaseOrderLine, SaleOrderLine, SaleOrder, Purchaser

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Purchaser)
# admin.site.register(SaleOrderLine)
# admin.site.register(PurchaseOrderLine)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('product_name', 'get_inventory_in_box', 'get_inventory_in_bottle', 'get_inventory_in_total')
    resources = ProductResource

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
