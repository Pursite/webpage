from django.contrib.auth.models import User
from ..models.user_model import UserProfile
from typing import Optional


def get_verified_user_with_credentials(username: str, phone_number: str) -> Optional[User]:
    """
    Checks if a user exists with the given username AND phone_number,
    and ensures the profile is verified.

    Returns the User object if all conditions match, otherwise returns None.
    """

    profile = UserProfile.objects.filter(
        username__username=username,
        phone_number=phone_number,
        is_verified=True
    ).select_related('username').first()

    return profile.username if profile else None