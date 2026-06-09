from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Order, OrderItem, ShippingInfo


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('product', 'quantity', 'unit_price', 'subtotal')


def get_status_badge(status):
    colors = {
        'pending': 'warning',
        'confirmed': 'info',
        'shipped': 'primary',
        'delivered': 'success',
        'cancelled': 'danger',
    }
    color = colors.get(status, 'secondary')
    return format_html('<span class="badge badge-{}" style="font-size: 12px; padding: 5px 10px;">{}</span>', color, status.title())


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'status_badge', 'payment_info', 'delivery_info', 'amount_display', 'placed_at')
    list_filter = ('status', 'payment_method', 'delivery_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('total_amount', 'created_at')
    inlines = [OrderItemInline]
    actions = ['mark_confirmed', 'mark_shipped', 'mark_delivered', 'mark_cancelled']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'status', 'total_amount')
        }),
        ('Delivery', {
            'fields': ('delivery_type', 'shipping_info')
        }),
        ('Payment', {
            'fields': ('payment_method',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def order_id(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.pk])
        return format_html('<a href="{}" style="font-weight: 600;">#ORD-{}</a>', url, obj.id)
    order_id.short_description = 'Order'

    def customer(self, obj):
        return format_html('{} <br/><small style="color: #666;">{}</small>', obj.user.username, obj.user.email)
    customer.short_description = 'Customer'
    customer.admin_order_field = 'user__username'

    def status_badge(self, obj):
        return get_status_badge(obj.status)
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def payment_info(self, obj):
        icons = {'cod': '💵', 'card': '💳', 'bkash': '📱', 'nagad': '📱'}
        icon = icons.get(obj.payment_method, '💳')
        return format_html('{} <span style="text-transform: capitalize;">{}</span>', icon, obj.get_payment_method_display())
    payment_info.short_description = 'Payment'

    def delivery_info(self, obj):
        return format_html('<span style="text-transform: capitalize;">{}</span>', obj.get_delivery_type_display())
    delivery_info.short_description = 'Delivery'

    def amount_display(self, obj):
        return format_html('<strong>৳ {}</strong>', obj.total_amount)
    amount_display.short_description = 'Total'
    amount_display.admin_order_field = 'total_amount'

    def placed_at(self, obj):
        delta = timezone.now() - obj.created_at
        if delta.days == 0:
            return format_html('<span style="color: #666;">Today, {}</span>', obj.created_at.strftime('%I:%M %p'))
        elif delta.days == 1:
            return 'Yesterday'
        return obj.created_at.strftime('%b %d, %Y')
    placed_at.short_description = 'Placed'
    placed_at.admin_order_field = 'created_at'

    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} order(s) marked as confirmed.')
    mark_confirmed.short_description = 'Mark selected as Confirmed'

    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} order(s) marked as shipped.')
    mark_shipped.short_description = 'Mark selected as Shipped'

    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_delivered.short_description = 'Mark selected as Delivered'

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} order(s) marked as cancelled.')
    mark_cancelled.short_description = 'Mark selected as Cancelled'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order_link', 'quantity', 'unit_price', 'subtotal_display')
    list_select_related = ('product', 'order')

    def order_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order_id])
        return format_html('<a href="{}">#ORD-{}</a>', url, obj.order_id)
    order_link.short_description = 'Order'

    def subtotal_display(self, obj):
        return format_html('<strong>৳ {}</strong>', obj.subtotal)
    subtotal_display.short_description = 'Subtotal'
    subtotal_display.admin_order_field = 'subtotal'


@admin.register(ShippingInfo)
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address_preview')
    search_fields = ('name', 'email', 'phone')

    def address_preview(self, obj):
        if len(obj.address) > 50:
            return obj.address[:50] + '...'
        return obj.address
    address_preview.short_description = 'Address'
