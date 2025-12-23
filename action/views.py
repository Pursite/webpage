from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from action.models import Comment
from action.serializers import CommentDetailSerializer, CommentCreateSerializer


class UserCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CommentCreateSerializer
        return CommentDetailSerializer

    def get_queryset(self):
        qs = Comment.objects.all()

        username = self.request.query_params.get("username")
        post_id = self.request.query_params.get("post")

        if username:
            qs = qs.filter(user__username=username)

        if post_id:
            qs = qs.filter(post_id=post_id)

        return qs

    def list(self, request, *args, **kwargs):
        pk = request.query_params.get("pk")
        if pk:  # دیتیل
            obj = get_object_or_404(self.get_queryset(), pk=pk)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        username = self.request.query_params.get("username")
        if not username:
            raise ValidationError({"error": "username is required"})

        user = User.objects.get(username=username)
        serializer.save(user=user)

