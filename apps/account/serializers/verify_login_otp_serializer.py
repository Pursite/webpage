from rest_framework import serializers
from django.core.validators import RegexValidator


class LoginVerifySerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message="Phone number must be 11 digits and formated like: '0912345678'."
    )

    username = serializers.CharField(
        max_length=150,
        required=True,
        allow_blank=False
    )

    phone_number = serializers.CharField(
        validators=[phone_regex],
        max_length=11,
        required=True
    )

    code = serializers.CharField(
        max_length=5,
        min_length=5,
        required=True
    )

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Verification code must contain digits")
        return value

    def validate_username(self, value):
        return value.strip()
