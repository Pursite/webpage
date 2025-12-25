from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from ..serializers.comment_create_serializer import CommentCreateSerializer
from ..serializers.comment_detail_serializer import CommentDetailSerializer


class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = CommentCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            comment = serializer.save(user=request.user)

            output_serializer = CommentDetailSerializer(comment)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


