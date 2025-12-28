from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from ..seializers.post_list_serializer import PostListSerializer
from ..selectors.selectors import post_list_selector
from ...lib.pagination import StandardPagePagination


class PostListAPIView(APIView):
    """
        Display a list of active advertisements.

        Features:
        - Filtering: Filter by 'product' ID or 'location'.
        - Searching: Search within 'caption' and 'location'.
        - Logic: Only displays posts where is_active=True.
        - Pagination: Implements StandardPagePagination.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'location']
    search_fields = ['caption', 'location']

    def get(self, request):
        """
            List all active posts with applied filters and pagination.
        """

        posts = post_list_selector(request=request, view=self)

        paginator = StandardPagePagination()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
