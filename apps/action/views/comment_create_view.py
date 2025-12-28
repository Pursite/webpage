from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from ..serializers.comment_create_serializer import CommentCreateSerializer
from ..serializers.comment_detail_serializer import CommentDetailSerializer
from ..services.services import comment_create_service


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
        comment = comment_create_service(user=request.user, data=request.data)

        output_serializer = CommentDetailSerializer(comment)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
