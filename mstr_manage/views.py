from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Customer, Product, Deliv_dest, Product_per_Customer
from .forms import ModelManageForm, CustomerForm
from io import TextIOWrapper
import csv
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

# Create your views here.

# Customer
# --------------------------------------
class CustomerList(ListView):
    model = Customer

    # def get_queryset(self):
    #     query = self.request.GET.get('q') 
    #     if query:
    #         # Q オブジェクトを使うと、ORでフィルター出来る。
    #         # https://docs.djangoproject.com/ja/2.1/topics/db/queries/#complex-lookups-with-q-objects
    #         return Customer.objects.filter(
    #             Q(code__icontains=query) | Q(name__icontains=query)
    #         )
    #     else:
    #         return Customer.objects.all()

class CustomerDetail(DetailView):

    model = Customer

class CustomerUpadate(UpdateView):
    model = Customer
    fields = '__all__'

# class CustomerUpadate(FormView):
#     template_name = "mstr_manage/customer_form.html"
#     form_class = CustomerForm
#     success_url = '/mstr_manage/customer'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

class CustomerCreate(CreateView):
    model = Customer
    fields = '__all__'

class CustomerDelete(DeleteView):
    model = Customer
    success_url = reverse_lazy('customer_list')

def get_customer_name_byajax(request):
    customer_code = request.POST.get('customer')
    obj = Customer.objects.get(code=customer_code)
    d = {
        'name': obj.name,
    }
    return JsonResponse(d)
# --------------------------------------



# Product
# --------------------------------------
class ProductList(ListView):
    model = Product
    
    # def get_queryset(self):
    #     query = self.request.GET.get('q') 
    #     if query:
    #         # Q オブジェクトを使うと、ORでフィルター出来る。
    #         # https://docs.djangoproject.com/ja/2.1/topics/db/queries/#complex-lookups-with-q-objects
    #         return Product.objects.filter(
    #             Q(code__icontains=query) | Q(name__icontains=query)
    #         )
    #     else:
    #         return Product.objects.all()


class ProductDetail(DetailView):
    model = Product

class ProductUpadate(UpdateView):
    model = Product
    fields = '__all__'


class ProductCreate(CreateView):
    model = Product
    fields = '__all__'


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')

def get_selling_price_byajax(request):
    selling_price_type = request.POST.get('selling_price_type')
    product_code = request.POST.get('p_code')
    obj = Product.objects.get(code=product_code)

    price = obj.selling_price

    d = {
        'price': price,
    }

    return JsonResponse(d)
    # return


# --------------------------------------



# Deliv_dest
# --------------------------------------
class Deliv_destList(ListView):
    model = Deliv_dest
    
    # def get_queryset(self):
    #     query = self.request.GET.get('q') 
    #     if query:
    #         # Q オブジェクトを使うと、ORでフィルター出来る。
    #         # https://docs.djangoproject.com/ja/2.1/topics/db/queries/#complex-lookups-with-q-objects
    #         return Deliv_dest.objects.filter(
    #             Q(code__icontains=query) | Q(name__icontains=query)
    #         )
    #     else:
    #         return Deliv_dest.objects.all()

        #     return Deliv_dest.objects.anotate(
        #         buff = FilteredRelation(query,),
        #     ).filter(
        #         Q(buff.code__icontains=query) | Q(buff.name__icontains=query)
        #     )
        # else:
        #     return Deliv_dest.objects.all()


class Deliv_destDetail(DetailView):
    model = Deliv_dest

class Deliv_destUpadate(UpdateView):
    model = Deliv_dest
    fields = '__all__'
    # fields = ['customer','code','name', 'checkname']

class Deliv_destCreate(CreateView):
    model = Deliv_dest
    fields = '__all__'
    # fields = ['customer','code','name', 'checkname']

class Deliv_destDelete(DeleteView):
    model = Deliv_dest
    success_url = reverse_lazy('deliv_dest_list')

# --------------------------------------



# Product_per_Customer
# --------------------------------------
class Product_per_CustomerList(ListView):
    model = Product_per_Customer
    
    # def get_queryset(self):
    #     query = self.request.GET.get('q') 
    #     if query:
    #         # Q オブジェクトを使うと、ORでフィルター出来る。
    #         # https://docs.djangoproject.com/ja/2.1/topics/db/queries/#complex-lookups-with-q-objects
    #         return Product_per_Customer.objects.filter(
    #             Q(code__icontains=query) | Q(name__icontains=query)
    #         )
    #     else:
    #         return Product_per_Customer.objects.all()


class Product_per_CustomerDetail(DetailView):
    model = Product_per_Customer

class Product_per_CustomerUpadate(UpdateView):
    model = Product_per_Customer
    fields = '__all__'
    # fields = ['customer','product','wholesale_price','prdct_code_by_cstmr']

class Product_per_CustomerCreate(CreateView):
    model = Product_per_Customer
    fields = '__all__'
    # fields = ['customer','product','wholesale_price','prdct_code_by_cstmr']

class Product_per_CustomerDelete(DeleteView):
    model = Product_per_Customer
    success_url = reverse_lazy('product_per_customer_list')



class Manage_Model(FormView):
    template_name = "mstr_manage/manage_model.html"
    form_class = ModelManageForm
    success_url = '/mstr_manage/'

    # This method is called when valid form data has been POSTed.
    def form_valid(self, form):
        
        model_type = form.cleaned_data['model_name']
        manage_type = form.cleaned_data['up_or_down']
        data = form.cleaned_data['data']

        if model_type == "customer":
            if manage_type == "up":
                customer_update(data)
        
        if model_type == "product":
            if manage_type == "up":
                product_update(data)

        elif model_type == "product_per_customer":
            if manage_type == "up":
                p_per_c_update(data)

        else:
            pass

        return super().form_valid(form)


# @login_required
def customer_update(file):
    data = TextIOWrapper(file, encoding='utf-8')
    csv_file = csv.reader(data, dialect='excel-tab')
    next(csv_file, None)

    for line in csv_file:
        c, created = Customer.objects.get_or_create(
                    code = line[0]
                )

        if created:
            c.name = line[1]
            c.save()
    return  

# @login_required
def product_update(file):
    data = TextIOWrapper(file, encoding='utf-8')
    csv_file = csv.reader(data, dialect='excel-tab')
    next(csv_file, None)


    for line in csv_file:
        # 商品の特定　なければ生成  
        p, created = Product.objects.get_or_create(
                    code = line[0]
                )

        #　新規のときだけデータ入れる。
        if created:
            p.name = line[1]
            p.alias = line[2]
            p.jancode = line[3]

        p.save()
    return  

# @login_required
def p_per_c_update(file):
    data = TextIOWrapper(file, encoding='utf-8')
    csv_file = csv.reader(data, dialect='excel-tab')
    next(csv_file, None)

    for line in csv_file:
        p_per_c = Product_per_Customer()
        
        p_per_c.customer = Customer.objects.get(code__exact=line[0])
        p_per_c.product = Product.objects.get(code__exact=line[2])
        p_per_c.wholesale_price = line[6]
        p_per_c.prdct_code_by_cstmr = line[7]

        p_per_c.save()

    return  
