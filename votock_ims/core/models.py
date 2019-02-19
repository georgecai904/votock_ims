from django.db import models

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="产品名称")
    sku = models.CharField(max_length=10, null=False, blank=False, verbose_name="产品编号")
    barcode = models.CharField(max_length=10, null=False, blank=False, verbose_name="条形编码")
    vintage = models.IntegerField(null=True, blank=True, verbose_name="产品年份")
    variety = models.CharField(max_length=20, null=True, blank=True, verbose_name="葡萄品种")
    region = models.CharField(max_length=20, null=True, blank=True, verbose_name="葡萄产区")
    pack_size = models.IntegerField(null=True, verbose_name="单箱数量")

    # inventory_in_box = models.IntegerField(editable=False, default=0, verbose_name="整箱库存")
    # inventory_in_bottle = models.IntegerField(editable=False, default=0, verbose_name="散装库存")
    #
    # inventory_in_total = models.IntegerField(editable=False, default=0,verbose_name="总库存（瓶）")

    def __str__(self):
        return f'{self.product_name}'

    class Meta:
        verbose_name = "产品信息"
        verbose_name_plural = "产品信息"

    def get_inventory_in_box(self):
        purchases = sum(i.quantity for i in PurchaseOrderLine.objects.filter(product=self, unit='box'))
        sales = sum(i.quantity for i in SaleOrderLine.objects.filter(product=self, unit='box'))
        return purchases - sales
    get_inventory_in_box.short_description = '整箱库存'

    def get_inventory_in_bottle(self):
        purchases = sum(i.quantity for i in PurchaseOrderLine.objects.filter(product=self, unit='bottle'))
        sales = sum(i.quantity for i in SaleOrderLine.objects.filter(product=self, unit='bottle'))
        return purchases - sales
    get_inventory_in_bottle.short_description = '散装库存'

    def get_inventory_in_total(self):
        return self.get_inventory_in_box() * self.pack_size + self.get_inventory_in_bottle()
    get_inventory_in_total.short_description = '总库存（瓶）'


class Supplier(models.Model):
    company_name = models.CharField(max_length=20, null=False, blank=False, verbose_name="公司名称")

    def __str__(self):
        return f'{self.company_name}'

    class Meta:
        verbose_name = "供应商"
        verbose_name_plural = "供应商"


class PurchaseOrder(models.Model):
    purchase_date = models.DateField(null=False, blank=False, verbose_name="采购日期")
    supplier = models.ForeignKey(Supplier, verbose_name="供货商", on_delete=models.CASCADE)
    contract_number = models.CharField(max_length=20, null=False, blank=False, verbose_name="采购单号")

    def __str__(self):
        return f'{self.purchase_date} - {self.supplier}'

    class Meta:
        verbose_name = "采购清单"
        verbose_name_plural = "采购清单"


class PurchaseOrderLine(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, verbose_name="采购单号")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="采购产品")
    quantity = models.IntegerField(null=False, blank=False, verbose_name="产品数量")
    UNIT_CHOICES = (
        ('box', '箱'),
        ('bottle', '瓶')
    )
    unit = models.CharField(max_length=10, null=False, blank=False, default='box', choices=UNIT_CHOICES,
                            verbose_name="数量单位")

    class Meta:
        verbose_name = "采购清单行"
        verbose_name_plural = "采购清单行"


class Purchaser(models.Model):
    purchaser_name = models.CharField(max_length=20, null=False, blank=False, verbose_name="顾客姓名")
    location = models.CharField(max_length=10, null=True, blank=True, verbose_name="所在区域")
    contact_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系方式")

    def __str__(self):
        return f'{self.purchaser_name}'

    class Meta:
        verbose_name = "采购商"
        verbose_name_plural = "采购商"


class SaleOrder(models.Model):
    sale_date = models.DateField(null=False, blank=False, verbose_name="销售日期")
    purchaser = models.ForeignKey(Purchaser, verbose_name="采购商", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sale_date} - {self.purchaser}'

    class Meta:
        verbose_name = "销售清单"
        verbose_name_plural = "销售清单"


class SaleOrderLine(models.Model):
    sale_order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, verbose_name="销售单号")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="销售产品")
    quantity = models.IntegerField(null=False, blank=False, verbose_name="产品数量")
    UNIT_CHOICES = (
        ('box', '箱'),
        ('bottle', '瓶')
    )
    unit = models.CharField(max_length=10, null=False, blank=False, default='箱', choices=UNIT_CHOICES,
                            verbose_name="数量单位")

    class Meta:
        verbose_name = "销售清单行"
        verbose_name_plural = "销售清单行"
