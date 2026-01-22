from rest_framework import serializers
from django.core.validators import RegexValidator


class LoginRequestSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'^09\d{9}$', message="Invalid phone format.")

    username = serializers.CharField(required=True)
    phone_number = serializers.CharField(validators=[phone_regex], max_length=11, required=True)