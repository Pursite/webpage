from django.urls import path
from page.views import PageView

urlpatterns = [
    path('', PageView.as_view(), name='page-view')
]



