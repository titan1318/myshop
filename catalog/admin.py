from django.contrib import admin
from .models import Product, Category, ContactInfo, Version


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address')
    search_fields = ('email',)
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created_at']
    search_fields = ['name', 'category__name']
    list_filter = ['available', 'category']


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['version_name', 'version_number', 'is_current']
    list_filter = ['is_current']
