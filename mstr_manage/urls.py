from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required 
# import views
urlpatterns = [
   path('', login_required(TemplateView.as_view(template_name="mstr_manage/index.html")), name='mstr_manage'),
   path('manage/',login_required(views.Manage_Model.as_view()), name='mstr_manage_manage'),
  
   path('customer/',login_required(views.CustomerList.as_view()), name='customer_list'),
   path('customer/<int:pk>/', login_required(views.CustomerDetail.as_view()), name='customer_detail'),
   path('customer/<int:pk>/update', login_required(views.CustomerUpadate.as_view()), name='customer_update'),
   path('customer/<int:pk>/delete', login_required(views.CustomerDelete.as_view()), name='customer_delete'),
   path('customer/create', login_required(views.CustomerCreate.as_view()), name='customer_create'),
   path('customer/getname', views.get_customer_name_byajax, name='get_customer_name_byajax'),

   path('product/',login_required(views.ProductList.as_view()), name='product_list'),
   path('product/<int:pk>/', login_required(views.ProductDetail.as_view()), name='product_detail'),
   path('product/<int:pk>/update', login_required(views.ProductUpadate.as_view()), name='product_update'),
   path('product/<int:pk>/delete', login_required(views.ProductDelete.as_view()), name='product_delete'),
   path('product/create', login_required(views.ProductCreate.as_view()), name='product_create'),
   path('product/getsellingprice', views.get_selling_price_byajax, name='get_selling_price_byajax'),
   
   path('deliv_dest/',login_required(views.Deliv_destList.as_view()), name='deliv_dest_list'),
   path('deliv_dest/<int:pk>/', login_required(views.Deliv_destDetail.as_view()), name='deliv_dest_detail'),
   path('deliv_dest/<int:pk>/update', login_required(views.Deliv_destUpadate.as_view()), name='deliv_dest_update'),
   path('deliv_dest/<int:pk>/delete', login_required(views.Deliv_destDelete.as_view()), name='deliv_dest_delete'),
   path('deliv_dest/create', login_required(views.Deliv_destCreate.as_view()), name='deliv_dest_create'),

   path('product_per_customer/',login_required(views.Product_per_CustomerList.as_view()), name='product_per_customer_list'),
   path('product_per_customer/<int:pk>/', login_required(views.Product_per_CustomerDetail.as_view()), name='product_per_customer_detail'),
   path('product_per_customer/<int:pk>/update', login_required(views.Product_per_CustomerUpadate.as_view()), name='product_per_customer_update'),
   path('product_per_customer/<int:pk>/delete', login_required(views.Product_per_CustomerDelete.as_view()), name='product_per_customer_delete'),
   path('product_per_customer/create', login_required(views.Product_per_CustomerCreate.as_view()), name='product_per_customer_create'),
]