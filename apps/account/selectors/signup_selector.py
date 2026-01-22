from django.contrib.auth.models import User
from ..models.user_model import UserProfile


def check_account_existence_for_signup(username: str, phone_number: str) -> dict:

    username_exists = User.objects.filter(username=username).exists()

    phone_exists = UserProfile.objects.filter(phone_number=phone_number).exists()

    return {
        "exists": username_exists or phone_exists,
        "username_taken": username_exists,
        "phone_taken": phone_exists
    }