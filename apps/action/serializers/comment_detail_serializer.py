from rest_framework import serializers
from apps.action.models.comment_model import PostComment


class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ("id", "text", "user", "parent", "replies", "created_at")

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentDetailSerializer(obj.replies.all(), many=True).data
        return []
