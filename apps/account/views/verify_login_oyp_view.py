from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from ..serializers.login_serializer import LoginVerifySerializer
from ..services.verify_login_otp_serivce import verify_login_otp_service


class LoginVerifyAPIView(APIView):
    """
    """
    permission_classes = []  # دسترسی برای همه باز است

    def post(self, request):
        serializer = LoginVerifySerializer(data=request.data)

        if serializer.is_valid():
            try:
                token_data = verify_login_otp_service(
                    username=serializer.validated_data['username'],
                    phone_number=serializer.validated_data['phone_number'],
                    received_code=serializer.validated_data['code']
                )

                return Response(token_data, status=status.HTTP_200_OK)

            except DjangoValidationError as e:
                return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({"error": "خطایی در تایید کد رخ داد."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)