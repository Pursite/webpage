from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle
from ..seializers.post_create_serializer import PostCreateSerializer
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
    serializer_class = PostCreateSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        """
            Validate and save a new post based on catalog products.
        """


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            AppLogger.log_activity(f"Post created id={post.id} for product={post.product_id}", user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        AppLogger.log_activity(f"Post create failed: {serializer.errors}", user=request.user, status="ERROR")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
