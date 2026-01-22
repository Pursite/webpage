from django.contrib import admin

from .models.category_brand_model import Category, Brand
from .models.product_image_model import ProductImage
from .models.product_model import Product


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at", "category", "brand")
    search_fields = ("user__username", "id")
    ordering = ("created_at",)
    readonly_fields = ("created_at", "modified_at")
    inlines = [ProductImageInline, ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
