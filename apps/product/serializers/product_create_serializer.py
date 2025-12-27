from rest_framework import serializers
from ..models.product_model import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    """
        Handles the creation of a new Product instance.

        Fields:
            user: Automatically handled in the view (marked as read-only).
            name, category, brand: Required input from the authorized admin.
    """

    class Meta:
        model = Product
        fields = ['user', 'name', 'category', 'brand']
        read_only_fields = ['user']
