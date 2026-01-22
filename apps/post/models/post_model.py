from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from apps.lib.basemodel import BaseModel
from apps.product.models.product_model import Product


class Post(BaseModel):
    """
        Represents a user-generated advertisement or listing for a product.

        This model links a specific product from the catalog to a user who
        wants to sell or showcase it. It includes pricing, location, and status.

        Attributes:
            product (ForeignKey): Reference to the master product from the catalog.
            user (ForeignKey): The user who created this listing/post.
            caption (TextField): A descriptive text provided by the user.
            location (CharField): Geographical location for the listing.
            price (DecimalField): The selling price set by the user.
            is_active (BooleanField): Toggle to show/hide the post from the public feed.
    """

    product = models.ForeignKey(Product, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    caption = models.TextField(_('caption'), blank=True)
    location = models.CharField(max_length=100, verbose_name=_('location'), blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name=_('Price'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        indexes = [
            models.Index(fields=['location', 'is_active']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
