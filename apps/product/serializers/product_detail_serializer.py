from rest_framework import serializers
from ..models.product_image import ProductImage
from ..models.product_model import Product


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_feature']


class ProductDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields = ["user", "name", "category", "brand_name", "images"]
