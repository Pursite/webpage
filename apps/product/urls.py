from django.urls import path

from .views.category_brand_view import CategoryListAPIView, BrandListAPIView
from .views.product_create_view import ProductCreateAPIView
from .views.product_list_view import ProductListAPIView
from .views.product_detail_view import ProductDetailAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('brands/', BrandListAPIView.as_view(), name='brand-list'),
    path('list/', ProductListAPIView.as_view(), name='product-base'),
    path('create/', ProductCreateAPIView.as_view(), name='product-base'),

    path('detail/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail-query'),
]
