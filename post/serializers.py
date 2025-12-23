from rest_framework import serializers
from action.serializers import CommentDetailSerializer
from post.models import Post


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id" ,"product", "title", "caption", "price", "user", 'comments')

    def get_comments(self, obj):
        return CommentDetailSerializer(obj.comments.all(), many=True).data


class PostCreateSerializer(serializers.ModelSerializer):
     class Meta:
        model = Post
        fields = ('product', 'title', 'caption', 'price', 'is_active')