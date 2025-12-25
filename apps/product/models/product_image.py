from django.db import models

from .product_model import Product


def product_image_path(instance, filename):
    return f"products/{instance.product.name}/{filename}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_path, verbose_name="Image")
    is_feature = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"