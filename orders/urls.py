from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    path('add/', views.order_add, name='order_add'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/edit/', views.order_edit, name='order_edit'),
    path('<int:order_id>/pdf/', views.order_pdf, name='order_pdf'),
    path('<int:order_id>/update_status/', views.update_order_status, name='update_order_status'),
    path('<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('export_month/', views.export_orders_month, name='export_orders_month'),
]
