from rest_framework import serializers
from ..models.comment_model import Comment
from ..serializers.comment_create_serializer import CommentCreateSerializer
from ...lib.loggers import AppLogger


def comment_create_service(user, data) -> Comment:
    """
    Handles comment/reply creation, validation, and logging.
    Raises ValidationError if data is invalid.
    """
    serializer = CommentCreateSerializer(data=data)

    try:
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(user=user)

        AppLogger.log_activity(
            f"Comment created id={comment.id} for Post={comment.post_id}",
            user=user
        )
        return comment

    except serializers.ValidationError as e:
        AppLogger.log_activity(
            f"Comment creation failed: {e.detail}",
            user=user,
            status="ERROR"
        )
        raise e
