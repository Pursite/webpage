from django.db import models
from .product_model import Product
import os, uuid


def product_image_path(instance, filename):
    """
        Generates a unique file path for uploaded product images.

        Uses UUID to prevent filename collisions and organizes images
        into folders based on the product ID.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"products/product_{instance.product.id}/{filename}"


class ProductImage(models.Model):
    """
        Stores multiple images for a single product.

        Attributes:
            product: Reference to the parent product.
            image: The actual image file.
            is_feature: Boolean flag to mark an image as the main/thumbnail image.
    """

    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_path, verbose_name="Image")
    is_feature = models.BooleanField(default=False)

    class Meta:
        unique_together = ['product', 'is_feature']


    def __str__(self):
        return f"Image for {self.product.name}"