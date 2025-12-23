from django.contrib.admin import register
from django.contrib import admin

from .models import Product

@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "user__username")
    ordering = ("-created_at",)
