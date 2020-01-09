from django.db import models
from django.utils import timezone
from mstr_manage.models import Customer, Product
from django.urls import reverse

# Create your models here.

#見積もり伝票

#header & footer
class Estimate_header(models.Model):
    

    ESTIMATE_STATE_CHOICES = [
        ("making", "作成中"),
        ("printed", "印刷済み"),
        ("onnego", "商談中"),
        ("success", "商談成立"),
        ("failed", "失注"),
    ]

    estimate_state = models.CharField(
        max_length=10,
        choices = ESTIMATE_STATE_CHOICES,
        default = "making",
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=300, null=True, blank=True) #顧客に表示する得意先名は自由に変更できるようにする。
    
    created_date = models.DateField(default=timezone.now)    #作成日
    valid_date = models.DateField(default=timezone.now, null=True, blank=True)    #見積もり期限 改定見積の場合の適用開始日
    
    sls_prn = models.CharField(max_length=300, null=True, blank=True) #担当
    sls_rep = models.CharField(max_length=300, null=True, blank=True) #承認

    wholesale_rate = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)    #掛け率　小数(decimal)で指定。

    remarks_1 = models.CharField(max_length=300, null=True, blank=True, default="上記価格に消費税は含まれておりません。")
    remarks_2 = models.CharField(max_length=300, null=True, blank=True)
    remarks_3 = models.CharField(max_length=300, null=True, blank=True)
    remarks_4 = models.CharField(max_length=300, null=True, blank=True)
    internal_remarks = models.TextField(null=True, blank=True)  #内部向けのメモ  
    
    def get_absolute_url(self):
       return reverse('estimate_header_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return (str(self.pk) + "_" + str(self.customer))

#detail
class Estimate_detail(models.Model):
    estmt_no = models.ForeignKey(Estimate_header, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    estimate_price = models.DecimalField(max_digits=7, decimal_places=2, null=True) # 使わない　fieldの削除が面倒なので放置する。

    selling_price_new = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    wholesale_price_new = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    wholesale_rate = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)    #掛け率　小数(decimal)で指定。
    remarks = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return (str(self.estmt_no) + "_" + str(self.product))

