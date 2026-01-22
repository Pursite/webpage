import random
from django.core.cache import cache
from django.core.exceptions import ValidationError
from ..selectors.login_selector import get_verified_user_with_credentials
from ..tasks.send_sms_task import send_otp_sms_task


def user_signin_service(username: str, phone_number: str):
    """
    Service to handle Login OTP request.
    1. Validates user existence and verification status.
    2. Generates a new OTP for login.
    3. Stores it in Redis and triggers Celery task.
    """

    user = get_verified_user_with_credentials(username=username, phone_number=phone_number)

    if not user:
        raise ValidationError("Invalid credentials or account not verified.")

    otp_code = str(random.randint(10000, 99999))

    cache_key = f"login_otp_{phone_number}"
    cache.set(cache_key, otp_code, timeout=120)

    send_otp_sms_task.delay(phone_number, otp_code)

    return user