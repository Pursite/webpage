from apps.product.models.product_model import Product


def product_list_selector(filters=None):
    """
    Fetches all products with optimized queries.
    Can be expanded to include prefetch_related for images.
    """
    queryset = Product.objects.all().select_related('category', 'brand').order_by('-created_at')

    if filters:
        queryset = queryset.filter(**filters)

    return queryset
