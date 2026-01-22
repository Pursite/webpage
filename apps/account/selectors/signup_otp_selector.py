from django.core.cache import cache

def get_otp_from_redis(phone_number: str) -> str:
    """
    Fetches the stored OTP for a specific phone number from Redis.
    """
    cache_key = f"otp_{phone_number}"
    return cache.get(cache_key)