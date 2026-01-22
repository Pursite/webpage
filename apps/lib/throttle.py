from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import AnonRateThrottle


class CustomThrottle(UserRateThrottle):
    scope = 'custom'


class SignupRateThrottle(AnonRateThrottle):
    rate = '5/hour'
