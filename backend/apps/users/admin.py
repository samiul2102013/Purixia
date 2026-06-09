from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff_badge', 'is_active_badge', 'date_joined_display')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'phone')
    list_select_related = True

    fieldsets = UserAdmin.fieldsets + (
        ('Contact Info', {'fields': ('phone',)}),
    )

    def is_staff_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span class="badge badge-danger">Superuser</span>')
        if obj.is_staff:
            return format_html('<span class="badge badge-warning">Staff</span>')
        return format_html('<span class="badge badge-secondary">User</span>')
    is_staff_badge.short_description = 'Role'
    is_staff_badge.admin_order_field = 'is_staff'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-success">Active</span>')
        return format_html('<span class="badge badge-danger">Inactive</span>')
    is_active_badge.short_description = 'Status'
    is_active_badge.admin_order_field = 'is_active'

    def date_joined_display(self, obj):
        return obj.date_joined.strftime('%b %d, %Y')
    date_joined_display.short_description = 'Joined'
    date_joined_display.admin_order_field = 'date_joined'
