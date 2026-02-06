from django.urls import path
from . import views

urlpatterns = [
    path('', views.clients_list, name='clients_list'),
    path('add/', views.client_create, name='client_add'),
    path('<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('<int:pk>/delete/', views.client_delete, name='client_delete'),
    path("ajax/add/", views.client_ajax_add, name="client_ajax_add"),
    path('delete/<int:pk>/', views.client_delete, name='client_delete'),



]
