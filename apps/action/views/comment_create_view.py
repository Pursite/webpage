from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from ..serializers.comment_create_serializer import CommentCreateSerializer
from ..serializers.comment_detail_serializer import CommentDetailSerializer
from ...lib.loggers import AppLogger

class CommentCreateAPIView(APIView):
    """
        Handle the creation of new comments or replies.

        Permissions:
            Only authenticated users can post comments.

        Throttling:
            Rate limiting is applied to prevent comment spam.

        Logging:
            Every successful comment is logged with its ID and associated Post ID.
    """


    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = CommentCreateSerializer

    def post(self, request):
        """
            Validate input data and save the comment instance.
            Returns the detailed representation of the created comment.
        """


        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            comment = serializer.save(user=request.user)
            AppLogger.log_activity(f"Comment created id={comment.id} for Post={comment.post_id}", user=request.user)
            output_serializer = CommentDetailSerializer(comment)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


