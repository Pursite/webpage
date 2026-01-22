from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.verify_signup_otp_serializer import VerifyOTPSerializer
from ..services.verify_signup_otp_service import verify_user_otp_service


class VerifySignUpOTPAPIView(APIView):
    """
    Endpoint to verify the OTP code sent to the user.
    """

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            try:
                verify_user_otp_service(
                    phone_number=serializer.validated_data['phone_number'],
                    received_code=serializer.validated_data['code']
                )
                return Response({"message": "Account verified successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)