from django.core.cache import cache
import os
from ..models.post_model import Post
from django.db import transaction
from ...lib.loggers import AppLogger
from rest_framework import serializers


def post_delete_service(post_id: int, user) -> None:
    """
    Business logic for safely deleting a post.
    Ensures ownership and logs security/activity events.
    """
    try:
        with transaction.atomic():
            post = Post.objects.filter(pk=post_id).select_for_update().first()

            if not post:
                AppLogger.log_security(f"Delete failed: Post {post_id} not found or unauthorized", user=user)
                raise serializers.ValidationError("Post not found or permission denied.")

            if post.user != user and not user.is_staff:
                AppLogger.log_security(f"Unauthorized delete attempt on post {post_id}", user=user)
                raise serializers.ValidationError("You do not have permission to delete this post.")
            image_paths = []
            if hasattr(post, 'product') and post.product:
                image_paths = list(post.product.images.values_list('image', flat=True))

            post_id_val = post.id
            post.delete()

            def clear_cache():
                cache.delete_pattern("post_list:*")
                cache.delete_pattern(f"post_detail:*'{post_id_val}'*")

                for relative_path in image_paths:
                    full_path = os.path.join("media", relative_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        AppLogger.log_activity(f"File deleted: {relative_path}", user=user)

            transaction.on_commit(clear_cache)

            AppLogger.log_activity(f"Post Deleted: ID {post_id_val}", user=user)

    except Exception as e:
        if not isinstance(e, serializers.ValidationError):
            AppLogger.log_activity(f"System error during post deletion: {str(e)}", user=user, status="CRITICAL")
        raise e
