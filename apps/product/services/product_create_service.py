from django.core.cache import cache
from rest_framework import serializers
from django.db import transaction
from apps.product.models.product_model import Product
from apps.product.serializers.product_create_serializer import ProductCreateSerializer
from apps.lib.loggers import AppLogger


def product_create_service(user, data) -> Product:
    """
    Creates a product. Uses atomic transaction to ensure data integrity
    between database save and activity logging.
    """
    serializer = ProductCreateSerializer(data=data, context={'user': user})

    try:
        with transaction.atomic():
            serializer.is_valid(raise_exception=True)
            product = serializer.save(user=user)
            transaction.on_commit(lambda: cache.delete_pattern("product:*"))
            AppLogger.log_activity(f"Product Created: {product.name} (ID: {product.id})", user=user)
            return product

    except serializers.ValidationError as e:
        AppLogger.log_activity(
            f"Product Creation Validation Failed: {e.detail}",
            user=user,
            status="ERROR"
        )
        raise e
    except Exception as e:
        AppLogger.log_activity(f"System Error in Product Creation: {str(e)}", user=user, status="CRITICAL")
        raise e
