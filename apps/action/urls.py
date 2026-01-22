from django.urls import path
from .views.comment_create_view import CommentCreateAPIView
from .views.comment_list_view import CommentListAPIView

app_name = 'action'

urlpatterns = [
    path('comments/add/', CommentCreateAPIView.as_view(), name='comment-create'),

    path('<int:post_id>/comments/', CommentListAPIView.as_view(), name='post-comments-list'),
]
