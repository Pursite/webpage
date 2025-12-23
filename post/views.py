from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from lib.pagination import StandardPagePagination
from post.models import Post
from post.serializers import PostDetailSerializer, PostCreateSerializer
from rest_framework import viewsets


class UserPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardPagePagination
    throttle_scope = 'custom'

    def get_queryset(self):
        username = self.request.query_params.get("username")
        qs = Post.objects.all()

        if username:
            qs = qs.filter(user__username=username)
        return qs

    def retrieve(self, request, *args, **kwargs):
        pk = request.query_params.get("pk")
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        pk = request.query_params.get("pk")
        if pk:
            obj = get_object_or_404(self.get_queryset(), pk=pk)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostCreateSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        username = self.request.query_params.get("username")
        if not username:
            raise ValidationError({"error": "username is required"})

        user = User.objects.get(username=username)
        serializer.save(user=user)