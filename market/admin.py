from django.contrib import admin

from .models import Product, Author


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'price', 'created_at']
    search_fields = ['name', 'author__username']
    list_filter = ['name', 'created_at']
    date_hierarchy = 'created_at'
    list_per_page = 10


@admin.register(Author)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_fields = ['username', 'email']
    list_filter = ['username']
