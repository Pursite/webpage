from rest_framework import serializers
from apps.action.serializers.comment_detail_serializer import CommentDetailSerializer
from ..models.post_model import Post
from ...product.serializers.product_list_serializer import ProductListSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    product = ProductListSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "product", "caption", "price", "user", 'comments')

    def get_comments(self, obj):
        main_comments = obj.comments.all().order_by('-created_at')[:10]
        return CommentDetailSerializer(main_comments, many=True).data