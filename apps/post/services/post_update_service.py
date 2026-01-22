from django.core.cache import cache
from rest_framework import serializers
from django.db import transaction
from ..models.post_model import Post
from ..serializers.post_create_serializer import PostCreateSerializer
from ...lib.loggers import AppLogger


def post_update_service(post_id: int, user, data: dict, partial: bool = False) -> Post:
    """
    Updates an existing post after verifying ownership.
    Utilizes atomic transactions to ensure consistency between data update and logging.
    """
    try:
        with transaction.atomic():
            post = Post.objects.select_for_update().filter(pk=post_id).first()

            if not post:
                raise serializers.ValidationError("Post not found.")

            if post.user != user and not user.is_staff:
                AppLogger.log_security(f"Unauthorized update attempt on post {post_id}", user=user)
                raise serializers.ValidationError("You do not have permission to edit this post.")

            serializer = PostCreateSerializer(post, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            updated_post = serializer.save(user=user)

            def clear_cache():
                cache.delete_pattern(f"post_detail:*'{post_id}'*")
                cache.delete_pattern("post_list:*")

            transaction.on_commit(clear_cache)

            mode = "PATCH" if partial else "PUT"
            AppLogger.log_activity(f"Post updated ({mode}) id={updated_post.id}", user=user)

            return updated_post

    except serializers.ValidationError as e:
        AppLogger.log_activity(f"Post update failed id={post_id}: {e.detail}", user=user, status="ERROR")
        raise e
    except Exception as e:
        if not isinstance(e, serializers.ValidationError):
            AppLogger.log_activity(f"Critical system error during update: {str(e)}", user=user, status="CRITICAL")
        raise e
