from rest_framework.exceptions import NotFound
from apps.product.models.product_model import Product


def product_detail_selector(product_id):
    """
        Retrieves a single product with images.
        If not found, raises DRF NotFound (404).
        """
    product = Product.objects.select_related('category', 'brand').prefetch_related('images').filter(
        pk=product_id).first()

    if not product:
        raise NotFound(detail="محصول مورد نظر یافت نشد.")

    return product
