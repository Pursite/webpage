from rest_framework import serializers
from ..models.category_brand_model import Brand, Category


class CategorySerializer(serializers.ModelSerializer):
    """
        Serializer for the Category model.
        Provides simple representation for category listings used in dropdowns or filters.
    """

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    """
        Serializer for the Brand model.
        Returns basic brand information for selection or display.
    """

    class Meta:
        model = Brand
        fields = ['id', 'name']
