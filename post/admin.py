from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "price", "created_at")
    list_filter = ("created_at", "price")
    search_fields = ("product__title", "user__username")
