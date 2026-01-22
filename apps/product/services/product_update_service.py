from django.core.cache import cache
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db import transaction
from apps.product.models.product_model import Product
from apps.product.serializers.product_create_serializer import ProductCreateSerializer
from apps.lib.loggers import AppLogger


def product_update_service(*, product_id: int, user, data: dict, partial: bool = False) -> Product:
    """
    Updates a product instance securely with atomic transaction and audit logging.
    """
    product = get_object_or_404(Product, pk=product_id)

    if not user.is_staff and product.user != user:
        AppLogger.log_activity(
            f"Unauthorized update attempt on Product ID: {product_id}",
            user=user,
            status="WARNING"
        )
        raise PermissionDenied("You do not have permission to update this product.")

    serializer = ProductCreateSerializer(
        product,
        data=data,
        partial=partial,
        context={'request': type('Mock', (object,), {'user': user})}
    )

    try:
        with transaction.atomic():
            serializer.is_valid(raise_exception=True)
            updated_product = serializer.save(user=user)

            def clear_cache():
                cache.delete_pattern(f"product:*product_detail_selector*'{product_id}'*")
                cache.delete_pattern("product:*product_list_selector*")

            transaction.on_commit(clear_cache)
            AppLogger.log_activity(f"Product Updated: ID {updated_product.id}", user=user)
            return updated_product

    except serializers.ValidationError as e:
        AppLogger.log_activity(
            f"Product Update Validation Failed: ID {product_id}, Errors: {e.detail}",
            user=user,
            status="ERROR"
        )
        raise e
