from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'unit_price', 'quantity', 'total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'shipping_name', 'total_price', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method']
    list_editable = ['status', 'payment_status']
    search_fields = ['order_number', 'shipping_name', 'shipping_email']
    readonly_fields = ['order_number', 'id', 'created_at']
    inlines = [OrderItemInline]
