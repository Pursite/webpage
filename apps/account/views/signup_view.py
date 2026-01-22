from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.signup_serializer import SignupSerializer


class SignupAPIView(APIView):
    """
    Handle User registration.
    Logic is encapsulated in the Service layer, called via Serializer.
    """

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "message": "User created successfully. OTP sent to your phone.",
                "username": user.username
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
