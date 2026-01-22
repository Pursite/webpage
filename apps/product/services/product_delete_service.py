from django.core.cache import cache
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from apps.product.models.product_model import Product
from apps.lib.loggers import AppLogger


def product_delete_service(*, product_id: int, user) -> bool:
    """
    Deletes a product after checking permissions and logs the event.
    Returns True if successful.
    """
    product = get_object_or_404(Product, pk=product_id)

    if not user.is_staff and product.user != user:
        AppLogger.log_activity(
            f"Unauthorized deletion attempt for Product ID: {product_id}",
            user=user,
            status="WARNING"
        )
        raise PermissionDenied("You do not have permission to delete this product.")

    try:
        with transaction.atomic():
            product_info = f"{product.name} (ID: {product.id})"

            product.delete()
            transaction.on_commit(lambda: cache.delete_pattern("product:*"))
            AppLogger.log_activity(f"Product Deleted Successfully: {product_info}", user=user)
            return True

    except Exception as e:
        AppLogger.log_activity(f"Error deleting product {product_id}: {str(e)}", user=user, status="CRITICAL")
        raise e
