from rest_framework import serializers
from apps.action.models.comment_model import Comment


class CommentDetailSerializer(serializers.ModelSerializer):
    """
        Provides a detailed view of a comment including its sub-replies.

        This serializer uses a recursive approach for 'replies' but only
        populates them for top-level comments (where parent_id is None).
    """


    user = serializers.CharField(source="user.username", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "text", "user", "parent", "replies", "created_at")

    def get_replies(self, obj):
        if obj.parent_id is None:
            return CommentDetailSerializer(obj.replies.all(), many=True).data
        return []


