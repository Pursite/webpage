from django.core.cache import cache
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ..models.user_model import UserProfile
from ..selectors.signup_selector import check_account_existence_for_signup
from ..tasks.send_sms_task import send_otp_sms_task
import random

from ...lib.loggers import AppLogger


def user_signup_service(username: str, phone_number: str) -> User:
    """
    Handles the logic for creating a new user and their associated profile.

    1. Checks if the account already exists using the selector.
    2. Creates a User instance and a UserProfile instance atomically.
    3. Generates an OTP and triggers a Celery task for SMS delivery.

    :param username: Unique username for the account.
    :param phone_number: Unique phone number for the profile.
    :return: The created User instance.
    :raises ValidationError: If the username or phone number is already taken.
    """

    existence_check = check_account_existence_for_signup(username=username, phone_number=phone_number)

    if existence_check['exists']:
        if existence_check['username_taken']:
            raise ValidationError("This username is already taken.")
        if existence_check['phone_taken']:
            raise ValidationError("This phone number is already registered.")

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=None
        )
        user.set_unusable_password()
        user.save()

        UserProfile.objects.create(
            username=user,
            phone_number=phone_number
        )
        AppLogger.log_activity(
            f"User Profile Created - {phone_number}",
            user=username
        )
    AppLogger.log_activity(
        f"Faild to create user",
        user=username
    )

    otp_code = str(random.randint(100000, 999999))
    cache_key = f"otp_{phone_number}"
    cache.set(cache_key, otp_code, timeout=120)
    send_otp_sms_task.delay(phone_number, otp_code)
    AppLogger.log_activity(f"OTP Task dispatched for {phone_number}")

    return user
