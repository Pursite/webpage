from django.contrib import admin
from .models.comment_model import PostComment


@admin.register(PostComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__is_active")
    raw_id_fields = ("user", "post")
    readonly_fields = ("created_at", "modified_at")