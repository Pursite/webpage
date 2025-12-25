from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from ..seializers.post_create_serializer import PostCreateSerializer


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = PostCreateSerializer
    throttle_classes = [UserRateThrottle, ]


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
