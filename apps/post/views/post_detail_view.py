from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..serializers.post_detail_serializer import PostDetailSerializer
from ..selectors.post_detail_selector import post_detail_selector
from ..services.post_update_service import post_update_service
from ..services.post_delete_service import post_delete_service
from ...lib.permissions import IsOwnerOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(600), name='dispatch')
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
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        post = post_update_service(post_id=pk, user=request.user, data=request.data, partial=True)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post_delete_service(post_id=pk, user=request.user)
        return Response({"detail": "Post Deleted"}, status=status.HTTP_204_NO_CONTENT)
