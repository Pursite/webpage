from rest_framework import serializers
from apps.product.models.product_model import Product
from apps.product.serializers.product_create_serializer import ProductCreateSerializer
from apps.lib.loggers import AppLogger


def product_create_service(user, data) -> Product:
    """
    Handles product creation and logging. 
    Raises ValidationError if data is invalid.
    """
    serializer = ProductCreateSerializer(data=data)

    try:
        serializer.is_valid(raise_exception=True)
        product = serializer.save(user=user)
        AppLogger.log_activity(f"Product Created: {product.name}", user=user)
        return product
    except serializers.ValidationError as e:
        AppLogger.log_activity(
            f"Product Creation Failed. Errors: {e.detail}",
            user=user,
            status="ERROR"
        )
        raise e


def product_update_service(product_id, user, data, partial=False) -> Product:
    """
    Handles full or partial product updates and logging. .
    """
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, pk=product_id)

    serializer = ProductCreateSerializer(product, data=data, partial=partial)

    try:
        serializer.is_valid(raise_exception=True)
        updated_product = serializer.save()
        AppLogger.log_activity(f"Product Updated ID: {updated_product.id}", user=user)
        return updated_product
    except serializers.ValidationError as e:
        AppLogger.log_activity(
            f"Product Update Failed ID: {product_id}. Errors: {e.detail}",
            user=user,
            status="ERROR"
        )
        raise e


def product_delete_service(product_id, user):
    """
    Handles product deletion and logging.
    """
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, pk=product_id)
    p_name, p_id = product.name, product.id

    product.delete()
    AppLogger.log_activity(f"Product Deleted: {p_name} (ID: {p_id})", user=user)
