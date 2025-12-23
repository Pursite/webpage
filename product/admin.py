from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "created_at")
    search_fields = ("user__username", "id")
    ordering = ("created_at",)
    readonly_fields = ("created_at", "modified_at")

    fieldsets = (
        (None, {
            "fields": ("title", "user")
        }),
        ("Meta info", {
            "fields": ("created_at", "modified_at"),
        }),
    )