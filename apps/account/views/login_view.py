from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from ..serializers.login_serializer import LoginRequestSerializer
from ..services.login_service import user_signin_service


class LoginRequestAPIView(APIView):

    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user_signin_service(
                    username=serializer.validated_data['username'],
                    phone_number=serializer.validated_data['phone_number']
                )

                return Response({
                    "message": "Code sent successfully",
                    "phone_number": serializer.validated_data['phone_number']
                }, status=status.HTTP_200_OK)

            except DjangoValidationError as e:
                return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

