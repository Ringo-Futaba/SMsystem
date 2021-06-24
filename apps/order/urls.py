from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import OrderListView, OrderInsertView, OrderDelView, OrderInfoView, OrderDelListView, OrderSearchByDateView,CountChartsView

urlpatterns = [
    path('order_list/', login_required(OrderListView.as_view()), name='list'),
    path('order_insert/', login_required(OrderInsertView.as_view()), name='insert'),
    path('order_delete/', login_required(OrderDelView.as_view()), name='delete'),
    path('order_info/', login_required(OrderInfoView.as_view()), name='info'),
    path('order_del_list/', login_required(OrderDelListView.as_view()), name='del_list'),
    path('order_search_date/', login_required(OrderSearchByDateView.as_view()), name='date_search'),
    path('order_count_charts/', login_required(CountChartsView.as_view()), name='count_charts')
]
