from django.urls import path
from action.views import UserCommentViewSet


comment_view = UserCommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', comment_view, name='comment-view'),
]