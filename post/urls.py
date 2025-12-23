from django.urls import path
from post.views import UserPostViewSet


post_view = UserPostViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('', post_view, name='post-view'),
]