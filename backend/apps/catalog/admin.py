from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display       = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'price', 'quantity', 'in_stock', 'rating')
    list_filter   = ('category', 'in_stock')
    search_fields = ('name', 'title')
    list_editable = ('price', 'quantity')
    inlines = [ProductImageInline]
