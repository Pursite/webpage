from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404
from ..models.post_model import Post
from ..seializers.post_create_serializer import PostCreateSerializer
from ..seializers.post_detail_serializer import PostDetailSerializer
from ...lib.permissions import IsOwnerOrReadOnly
from ...lib.loggers import AppLogger


class PostDetailAPIView(APIView):
    """
        Manage individual posts: View, Update (Full/Partial), or Delete.

        Security:
        - Permissions: IsAuthenticatedOrReadOnly + IsOwnerOrReadOnly.
        - Manual Check: Uses check_object_permissions to ensure only the owner can modify.

        Features:
        - Soft Check: Hidden posts (is_active=False) return a 404 response to the public.
    """


    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, pk):
        """
            Retrieve post details. Returns 404 if the post is inactive.
        """


        post = get_object_or_404(Post, pk=pk)

        if not post.is_active:
            return Response(
                {"detail": "Post Not Available"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostDetailSerializer(post)

        return Response(serializer.data)

    def patch(self, request, pk):
        """
            Partially update post fields (e.g., price or caption).
        """


        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)

        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            AppLogger.log_activity(f"Post patched id={post.id}", user=request.user)
            return Response(serializer.data)

        AppLogger.log_activity(f"Post patch failed id={post.id}", user=request.user, status="ERROR")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
                Complete update of the post instance.
        """


        post = get_object_or_404(Post, pk=pk)

        self.check_object_permissions(request, post)

        serializer = PostCreateSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()

            AppLogger.log_activity(
                msg=f"Post updated (PUT) | post_id={post.id}",
                user=request.user
            )

            return Response(serializer.data)

        AppLogger.log_activity(
            msg=f"Post update (PUT) failed | post_id={post.id} | errors={serializer.errors}",
            user=request.user,
            status="ERROR"
        )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
                Delete a post and log the action.
        """


        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)

        p_id = post.id
        post.delete()

        AppLogger.log_activity(f"Post DELETED id={p_id}", user=request.user)
        return Response({"detail": "Post Deleted"}, status=status.HTTP_204_NO_CONTENT)


