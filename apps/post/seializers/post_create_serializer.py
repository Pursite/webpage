from rest_framework import serializers
from ..models.post_model import Post


class PostCreateSerializer(serializers.ModelSerializer):
    """
        Serializer for creating and updating user posts.

        Features:
        - Automatically retrieves 'user' from the context (marked as read-only).
        - Includes custom field validation for 'price'.
    """


    user = serializers.CharField(source='user.username', read_only=True)

    def validate_price(self, value):
        """
            Check that the price is a positive value.

            Args:
                value (Decimal): The price value to be validated.
            Raises:
                ValidationError: If price is less than or equal to 0.
        """


        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    class Meta:
        model = Post
        fields = ('product', 'user', 'caption', 'price', "location", 'is_active')