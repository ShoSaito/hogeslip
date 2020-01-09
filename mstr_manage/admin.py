from django.contrib import admin
from .models import Customer, Product, Deliv_dest, Product_per_Customer

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Deliv_dest)
admin.site.register(Product_per_Customer)
