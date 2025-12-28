from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle
from ..seializers.post_create_serializer import PostCreateSerializer
from ..services.services import post_create_service
from ...lib.loggers import AppLogger


class PostCreateAPIView(APIView):
    """
        Handle the creation of new user-generated advertisements (posts).

        Features:
        - Permissions: IsAuthenticatedOrReadOnly (Users must be logged in to post).
        - Throttling: UserRateThrottle prevents spamming post creation.
        - Logic: Automatically associates the post with the authenticated user.
        - Logging: Tracks successful creation and validation errors.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        """
            Validate and save a new post based on catalog products.
        """

        post = post_create_service(user=request.user, data=request.data)
        serializer = PostCreateSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
