from django.urls import path

from .views.login_view import LoginRequestAPIView
from .views.signup_view import SignupAPIView
from .views.verify_signup_otp_view import VerifySignUpOTPAPIView


urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name="signup"),
    path('signup/verifyotp/', VerifySignUpOTPAPIView.as_view(), name="verify-signup-otp"),
    path('login/', LoginRequestAPIView.as_view(), name="login"),
]
