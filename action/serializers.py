from rest_framework import serializers
from action.models import Comment



class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "text", "user", "post", "created_time")

    def get_post(self, obj):
        return {
            "id": obj.post.id,
            "caption": obj.post.caption,
            "product": obj.post.product.title,
        }


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text", "post")