from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from ..selectors.login_selector import get_verified_user_with_credentials
from apps.lib.loggers import AppLogger


def verify_login_otp_service(username: str, phone_number: str, received_code: str) -> dict:

    cache_key = f"login_otp_{phone_number}"
    stored_code = cache.get(cache_key)

    if not stored_code:
        AppLogger.log_security(f"Attempted login with expired/non-existent OTP for {phone_number}")
        raise ValidationError("OTP code expired")

    if stored_code != received_code:
        AppLogger.log_security(f"Invalid OTP entered for {phone_number}")
        raise ValidationError("invalid Code entered")

    user = get_verified_user_with_credentials(username=username, phone_number=phone_number)

    if not user:
        raise ValidationError("information not valid or user profile not found")

    cache.delete(cache_key)

    refresh = RefreshToken.for_user(user)

    AppLogger.log_activity(f"User {username} logged in successfully via OTP.")

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'username': user.username
    }