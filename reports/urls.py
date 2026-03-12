# reports/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_dashboard, name='reports_dashboard'),
    path('export-excel/', views.export_reports_excel, name='export_reports_excel'),
    path('export_pdf/', views.reports_pdf, name='reports_pdf'),
]