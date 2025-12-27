from rest_framework import serializers
from apps.action.serializers.comment_detail_serializer import CommentDetailSerializer
from ..models.post_model import Post
from ...product.serializers.product_list_serializer import ProductListSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    """
        Comprehensive serializer for single post retrieval.

        Includes:
        - 'product': Full details of the product using ProductListSerializer.
        - 'comments': A curated list of the top 10 recent parent comments.
    """


    user = serializers.CharField(source='user.username', read_only=True)
    product = ProductListSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "product", "caption", "price", "user", 'comments')

    def get_comments(self, obj):
        """
            Retrieves the 10 most recent root comments for this post.
            Filters out replies to prevent nested overload in the detail view.
        """


        main_comments = obj.comments.filter(parent__isnull=True).order_by('-created_at')[:10]
        return CommentDetailSerializer(main_comments, many=True).data
