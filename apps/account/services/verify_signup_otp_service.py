from django.core.exceptions import ValidationError
from ..models.user_model import UserProfile
from ..selectors.signup_otp_selector import get_otp_from_redis


def verify_user_otp_service(phone_number: str, received_code: str) -> bool:
    stored_code = get_otp_from_redis(phone_number)

    if not stored_code:
        raise ValidationError("OTP expired or not found.")

    if stored_code != received_code:
        raise ValidationError("Invalid OTP code.")

    profile = UserProfile.objects.filter(phone_number=phone_number).first()
    if not profile:
        raise ValidationError("User profile not found.")

    profile.is_verified = True
    profile.save()

    from django.core.cache import cache
    cache.delete(f"otp_{phone_number}")

    return True