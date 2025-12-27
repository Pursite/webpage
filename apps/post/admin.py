from django.contrib import admin
from .models.post_model import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "short_caption", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("user__username",)
    raw_id_fields = ("user", "product")
    readonly_fields = ("created_at", "modified_at")

    def short_caption(self, obj):
        return (obj.caption[:30] + "...") if obj.caption and len(obj.caption) > 30 else obj.caption

    short_caption.short_description = "Caption"
