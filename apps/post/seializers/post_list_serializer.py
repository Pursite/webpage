from rest_framework import serializers
from ..models.post_model import Post


class PostListSerializer(serializers.ModelSerializer):
    """
        Lightweight serializer for displaying multiple posts in a feed.

        Optimized to return only essential information, including
        the product name and basic listing details.
    """


    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'product_name', 'caption', 'price', 'location', 'created_at', 'is_active']
