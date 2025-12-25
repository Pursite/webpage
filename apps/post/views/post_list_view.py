from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models.post_model import Post
from ..seializers.post_create_serializer import PostCreateSerializer
from ..seializers.post_list_serializer import PostListSerializer
from ...lib.pagination import StandardPagePagination


class PostListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostListSerializer
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'user', 'location']
    search_fields = ['caption', "location"]

    def get(self, request):
        posts = Post.objects.filter(is_active=True).order_by('-created_at')

        for backend in list(self.filter_backends):
            posts = backend().filter_queryset(request, posts, self)

        paginator = StandardPagePagination()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

