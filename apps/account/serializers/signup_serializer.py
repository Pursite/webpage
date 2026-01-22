from rest_framework import serializers
from django.core.validators import RegexValidator
from ..services.signup_service import user_signup_service
from django.core.exceptions import ValidationError as DjangoValidationError


class SignupSerializer(serializers.Serializer):

    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message="Phone number must be entered in the format: '09123456789'. Up to 11 digits allowed."
    )

    username = serializers.CharField(
        max_length=150,
        required=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )

    phone_number = serializers.CharField(
        validators=[phone_regex],
        max_length=11,
        required=True
    )

    def save(self, validated_data):
        try:
            user = user_signup_service(
                username=validated_data['username'],
                phone_number=validated_data['phone_number']
            )
            return user
        except DjangoValidationError as e:
            raise serializers.ValidationError(detail={"error": str(e)})

    def update(self, instance, validated_data):
        pass