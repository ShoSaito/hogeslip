from django.db import models
from django.urls import reverse
from django.utils import timezone

import os
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
# Create your models here.


#得意先
class Customer(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=32)
    email = models.EmailField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, help_text="ロゴなど。アップロード可能な形式はpng or jpg",\
         upload_to='customers', validators=[FileExtensionValidator(['png','jpg' ])],)
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return (str(self.code) + " - " + str(self.name))

    def get_absolute_url(self):
       return reverse('customer_detail', kwargs={'pk': self.pk})

#商品
class Product(models.Model):
    AREA = (
        ('north', 'north'),
        ('middle', 'middle'),
        ('south', 'south'),
    )
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=32)
    area = models.CharField(max_length=16, choices=AREA, default="0", \
                            verbose_name="販売エリア", help_text='主な販売地域')
    selling_price = models.DecimalField( max_digits=7, 
                                        decimal_places=2, null=True)
    image = models.FileField(null=True, blank=True,
                            upload_to='products',
                            validators=[FileExtensionValidator(['png','jpg' ])],)

    def __str__(self):
        return (str(self.code) + " - " + str(self.name))

    def get_absolute_url(self):
       return reverse('product_detail', kwargs={'pk': self.pk})

#納品先
class Deliv_dest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,verbose_name='得意先')
    code = models.IntegerField()
    name = models.CharField(max_length=32)
    
    #顧客ごとに納品先コードはユニーク
    class Meta:
        #django 2.2以降は非推奨 https://docs.djangoproject.com/en/2.2/ref/models/options/#unique-together 
        # unique_together = ('customer', 'code')
        constraints = [
            models.UniqueConstraint(fields=['customer', 'code'], name='unique_deliv_dest')
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
       return reverse('deliv_dest_detail', kwargs={'pk': self.pk})

class Product_per_Customer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="得意先")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    wholesale_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="卸値")

    #顧客ごとに製品はユニーク
    class Meta:
        #django 2.2以降は非推奨 https://docs.djangoproject.com/en/2.2/ref/models/options/#unique-together 
        # unique_together = ('customer', 'product')
        constraints = [
            models.UniqueConstraint(fields=['customer', 'product'], name='unique_product')
        ]

    def __str__(self):
        return (str(self.customer) + " / " + str(self.product))

    def get_absolute_url(self):
       return reverse('product_per_customer_detail', kwargs={'pk': self.pk})