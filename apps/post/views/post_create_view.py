from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from ..serializers.post_create_serializer import PostCreateSerializer
from ..services.post_create_service import post_create_service


class PostCreateAPIView(APIView):
    """
    API View to handle post creation.
    Ensures the user is authenticated and enforces rate limiting.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        post = post_create_service(user=request.user, data=request.data)
        serializer = PostCreateSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
