# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_list, name='services_list'),
    path('add/', views.service_add, name='service_add'),
    path('<int:service_id>/edit/', views.service_edit, name='service_edit'),
    path('<int:service_id>/delete/', views.service_delete, name='service_delete'),
    path("ajax/add/", views.service_ajax_add, name="service_ajax_add"),
    path('delete/<int:pk>/', views.service_delete, name='service_delete'),


]
