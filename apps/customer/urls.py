from django.contrib import admin
from django.urls import path, include
from .views import CustomerListView, CustomerInsertView, CustomerDelView, CustomerUpdateView, CustomerInfoView, CustomerDelListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('customer_list/', login_required(CustomerListView.as_view()), name='List'),
    path('customer_insert/',login_required(CustomerInsertView.as_view()), name='insert'),
    path('customer_del/', login_required(CustomerDelView.as_view()), name='delete'),
    path('customer_update/', login_required(CustomerUpdateView.as_view()), name='update'),
    path('customer_info/', login_required(CustomerInfoView.as_view()), name='info'),
    path('customer_dellist/', login_required(CustomerDelListView.as_view()), name='delList')
]
