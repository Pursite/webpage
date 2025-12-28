from rest_framework import serializers
from ..models.product_image_model import ProductImage
from ..models.product_model import Product


class ProductImageSerializer(serializers.ModelSerializer):
    """
        Serializes product images.
        Returns the file URL and whether it's the featured image for the product.
    """

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_feature']


class ProductDetailSerializer(serializers.ModelSerializer):
    """
        Provides a comprehensive view of a single product.

        Includes:
            - Flattened data for brand and category titles (using 'source').
            - Nested list of all images related to the product.
            - The username of the admin who created the record.
    """

    user = serializers.CharField(source='user.username', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields = ["user", "name", "category", "brand_name", "images"]
