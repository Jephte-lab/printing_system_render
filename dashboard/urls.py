# dashboard/urls.py
from django.urls import path
from . import views
from .views import dashboard_home
from services import views as service_views


urlpatterns = [
    path('services/', service_views.services_list, name='services_list'),
    path('', views.dashboard_home, name='dashboard_home'),
    path('update-status/', views.update_order_status, name='update_order_status'),
        # Clients
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/add/', views.client_add, name='client_add'),
    path('clients/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('orders/', views.orders_list, name='orders_list'),
    # Add these for management links
    path('services/', service_views.services_list, name='services_list'),
    path('orders/', views.orders_list, name='orders_list'),
    path('update-status/', views.update_order_status, name='update_order_status'),
    path('clients/edit/<int:pk>/', views.client_edit, name='client_edit'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/add/', views.add_staff, name='add_staff'),
    path('users/<int:user_id>/staff/', views.toggle_staff, name='toggle_staff'),
    path('users/<int:user_id>/active/', views.toggle_active, name='toggle_active'),

]
