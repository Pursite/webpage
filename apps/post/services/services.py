from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ..models.post_model import Post
from ..seializers.post_create_serializer import PostCreateSerializer
from ...lib.loggers import AppLogger


def post_create_service(user, data) -> Post:
    """
    Handles post creation, validation, and activity logging.
    Raises serializers.ValidationError if data is incorrect.
    """
    serializer = PostCreateSerializer(data=data)

    try:
        serializer.is_valid(raise_exception=True)
        post = serializer.save(user=user)
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


def post_update_service(post_id, user, data, partial=False) -> Post:
    """
    Updates an existing post. Checks ownership and logs all outcomes.
    English docstrings are maintained as requested.
    """
    post = get_object_or_404(Post, pk=post_id)

    if post.user != user:
        AppLogger.log_security(f"Unauthorized update attempt on post {post_id}", user=user)
        raise serializers.ValidationError("You do not have permission to edit this post.")

    serializer = PostCreateSerializer(post, data=data, partial=partial)

    try:
        serializer.is_valid(raise_exception=True)
        updated_post = serializer.save()

        mode = "PATCH" if partial else "PUT"
        AppLogger.log_activity(f"Post updated ({mode}) id={updated_post.id}", user=user)
        return updated_post

    except serializers.ValidationError as e:
        AppLogger.log_activity(f"Post update failed id={post_id}: {e.detail}", user=user, status="ERROR")
        raise e


def post_delete_service(post_id, user):
    """
    Deletes a post after confirming ownership.
    """
    post = get_object_or_404(Post, pk=post_id)

    if post.user != user:
        AppLogger.log_security(f"Unauthorized delete attempt on post {post_id}", user=user)
        raise serializers.ValidationError("You do not have permission to delete this post.")

    p_id = post.id
    post.delete()
    AppLogger.log_activity(f"Post DELETED id={p_id}", user=user)
