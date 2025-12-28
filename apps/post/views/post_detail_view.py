from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..seializers.post_create_serializer import PostCreateSerializer
from ..seializers.post_detail_serializer import PostDetailSerializer
from ..selectors.selectors import post_detail_selector
from ..services.services import post_update_service, post_delete_service
from ...lib.permissions import IsOwnerOrReadOnly


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
        post = post_detail_selector(post_id=pk, user=request.user)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = post_update_service(post_id=pk, user=request.user, data=request.data, partial=False)
        serializer = PostCreateSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        post = post_update_service(post_id=pk, user=request.user, data=request.data, partial=True)
        serializer = PostCreateSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post_delete_service(post_id=pk, user=request.user)
        return Response({"detail": "Post Deleted"}, status=status.HTTP_204_NO_CONTENT)
