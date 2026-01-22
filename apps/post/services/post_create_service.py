from django.core.cache import cache
from rest_framework import serializers
from ..models.post_model import Post
from ..serializers.post_create_serializer import PostCreateSerializer
from ...lib.loggers import AppLogger
from django.db import transaction


def post_create_service(user, data) -> Post:
    """
    Handles post creation, validation, and activity logging.
    Raises serializers.ValidationError if data is incorrect.
    """
    serializer = PostCreateSerializer(data=data)

    try:
        with transaction.atomic():
            serializer.is_valid(raise_exception=True)
            post = serializer.save(user=user)
            transaction.on_commit(lambda: cache.delete_pattern("post_list:*"))
            AppLogger.log_activity(
                f"Post created id={post.id} for product={post.product_id}",
                user=user
            )
            return post

    except serializers.ValidationError as e:
        AppLogger.log_activity(
            f"Post create failed: {e.detail}",
            user=user,
            status="ERROR"
        )
        raise e
    except Exception as e:
        AppLogger.log_activity(f"System error in post creation: {str(e)}", user=user, status="CRITICAL")
        raise e
