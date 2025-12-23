from rest_framework import serializers
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'user')

    def get_posts(self, obj):
        return obj.posts.count()
