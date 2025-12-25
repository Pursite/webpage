from rest_framework import serializers

from ..models.product_model import Product


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['user', 'name', 'category', 'brand']
        read_only_fields = ['user']
