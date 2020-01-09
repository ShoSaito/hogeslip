from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.urls import reverse_lazy
from .models import Estimate_header, Estimate_detail
from mstr_manage.models import Customer, Product
from math import ceil
from .forms import Estimate_headerForm, Estimate_detailFormSet, ModelManageForm
from django.contrib.auth.decorators import login_required
from django.views import View


# Create your views here.

class Estimate_headerList(ListView):
    model = Estimate_header
    ordering = ['-pk']

class Estimate_headerDetail(DetailView):
    model = Estimate_header

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estimate_headers = Estimate_header.objects.filter(pk=self.kwargs.get('pk'))
        context['estimate_details'] = Estimate_detail.objects.filter(estmt_no__in=estimate_headers)
        return context

class Estimate_headerUpadate(UpdateView):
    model = Estimate_header
    form_class = Estimate_headerForm



class Estimate_headerCreate(CreateView):
    model = Estimate_header
    form_class = Estimate_headerForm




class Estimate_headerDelete(DeleteView):
    model = Estimate_header
    success_url = reverse_lazy('estimate_header_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estimate_headers = Estimate_header.objects.filter(pk=self.kwargs.get('pk'))
        context['estimate_details'] = Estimate_detail.objects.filter(estmt_no__in=estimate_headers)
        return context

class Estimate_headerPrint(DetailView):
    model = Estimate_header
    template_name = 'estimate/estimate_print.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estimate_headers = Estimate_header.objects.filter(pk=self.kwargs.get('pk'))

        estimate_details = Estimate_detail.objects.filter(estmt_no__in=estimate_headers)
        context['estimate_details'] = estimate_details
        
        DETAIL_PER_PAGE = 7
        pages = ceil(estimate_details.count()/DETAIL_PER_PAGE)
        context['pages'] = pages

        return context

