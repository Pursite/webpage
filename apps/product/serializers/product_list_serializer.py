from rest_framework import serializers
from .product_detail_serializer import ProductImageSerializer
from ..models.product_model import Product


class ProductListSerializer(serializers.ModelSerializer):
    """
        Optimized serializer for product list displays.

        Instead of returning all images, it returns a single 'thumbnail'
        to reduce payload size and improve load speed for mobile/web clients.
    """

    user = serializers.CharField(source='user.username', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'user', 'brand_name', 'category_title', 'thumbnail']

    def get_thumbnail(self, obj):
        """
            Custom logic to retrieve the primary image for the product.
            Priority:
            1. The image marked as 'is_feature'.
            2. The first image in the collection.
            3. Returns None if no images are found.

            Builds an absolute URI if the request context is available.
        """

        image = obj.images.filter(is_feature=True).first() or obj.images.first()
        if image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url
        return None
