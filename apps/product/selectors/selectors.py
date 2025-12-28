from rest_framework.generics import get_object_or_404

from apps.product.models.product_model import Product


def product_list_selector(filters=None):
    """
    Fetches all products with optimized queries.
    Can be expanded to include prefetch_related for images.
    """
    queryset = Product.objects.all().order_by('-created_at')
    return queryset


def product_detail_selector(product_id):
    """
    Retrieves a single product or raises 404.
    Optimized to fetch related images in one query.
    """
    return get_object_or_404(Product.objects.prefetch_related('images'), pk=product_id)
