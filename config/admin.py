from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

class AdminSite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser

admin_site = AdminSite(name='secure_admin')
