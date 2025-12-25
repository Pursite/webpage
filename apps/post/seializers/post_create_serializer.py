from rest_framework import serializers
from ..models.post_model import Post


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("قیمت باید بزرگتر از صفر باشد.")
        return value

    class Meta:
        model = Post
        fields = ('product', 'user', 'caption', 'price', "location", 'is_active')
