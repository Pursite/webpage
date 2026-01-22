from rest_framework import serializers
from django.core.validators import RegexValidator


class VerifyOTPSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'^09\d{9}$', message="Invalid phone format.")

    phone_number = serializers.CharField(validators=[phone_regex], max_length=11)
    code = serializers.CharField(max_length=6)  