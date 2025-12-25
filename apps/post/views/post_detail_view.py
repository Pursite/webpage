from rest_framework.generics import get_object_or_404
from ..seializers.post_create_serializer import PostCreateSerializer
from ..seializers.post_detail_serializer import PostDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models.post_model import Post
from ...lib.permissions import IsOwnerOrReadOnly


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if not post.is_active:
            return Response({"detail": "Post Not Available"}, status=404)

        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)

        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostCreateSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)