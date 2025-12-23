from django.urls import path
from product.views import ProductViewSet


product_view = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', product_view, name='product-view'),
]