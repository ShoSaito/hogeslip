from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required 
# import views
urlpatterns = [
   path('',login_required(views.Estimate_headerList.as_view()), name='estimate_header_list'),
   path('<int:pk>/', login_required(views.Estimate_headerDetail.as_view()), name='estimate_header_detail'),
   path('<int:pk>/update', login_required(views.Estimate_headerUpadate.as_view()), name='estimate_header_update'),
   path('create', login_required(views.Estimate_headerCreate.as_view()), name='estimate_header_create'),
   path('<int:pk>/delete', login_required(views.Estimate_headerDelete.as_view()), name='estimate_header_delete'),
   path('<int:pk>/print', login_required(views.Estimate_headerPrint.as_view()), name='estimate_header_print'),
]