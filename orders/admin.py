from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'name', 'created_at', 'total_price', 'pdf_link')
    inlines = [OrderItemInline]
    list_filter = ('created_at',)
    search_fields = ('client__name',)

    def pdf_link(self, obj):
        return format_html('<a class="button" href="/orders/{}/pdf/" target="_blank">Generate PDF</a>', obj.id)

    pdf_link.short_description = "PDF Receipt"
    pdf_link.allow_tags = True
