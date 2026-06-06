from django.contrib import admin
from .models import Order, OrderItem, ShippingInfo


class OrderItemInline(admin.TabularInline):
    model          = OrderItem
    extra          = 0
    readonly_fields = ('subtotal',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'total_amount', 'created_at')
    list_filter  = ('status', 'payment_method', 'delivery_type')
    inlines      = [OrderItemInline]


@admin.register(ShippingInfo)
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')