from django.urls import path
from .views.comment_create_view import CommentCreateAPIView
from .views.comment_list_api import CommentListAPIView


urlpatterns = [
    path('comments/add/', CommentCreateAPIView.as_view(), name='add-comment'),

    path('<int:post_id>/comments/', CommentListAPIView.as_view(), name='post-comments-list'),
]