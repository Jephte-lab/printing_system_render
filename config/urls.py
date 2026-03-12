from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        '',
        auth_views.LoginView.as_view(template_name='dashboard/login.html'),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', include('dashboard.urls')),
    path('orders/', include('orders.urls')),
    path('clients/', include('clients.urls')),
    path('services/', include('services.urls')),
    path("expenses/", include("expenses.urls")),
    path('reports/', include('reports.urls')),

    # ✅ leave admin EXACTLY like this
    path('admin/', admin.site.urls),
]
