from django.urls import path
from .views.post_detail_view import PostDetailAPIView
from .views.post_list_view import PostListAPIView
from .views.post_create_view import PostCreateAPIView

app_name = 'post'

urlpatterns = [
    path('list/', PostListAPIView.as_view(), name='post-list'),
    path('create/', PostCreateAPIView.as_view(), name='post-create'),
    path('detail/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
]
