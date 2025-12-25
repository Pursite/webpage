from rest_framework import serializers
from ..models.product_model import Product


class ProductListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields = 'id', 'name', 'user', 'brand_name', 'category_title'