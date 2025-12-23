from rest_framework import serializers
from rest_framework import serializers
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user.username')

    class Meta:
        model = Product
        fields = ('id', 'title')