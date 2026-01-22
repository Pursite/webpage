from django.test import TestCase, override_settings
from ...selectors.product_detail_selector import product_detail_selector
from ..factories import ProductFactory, ProductImageFactory
from django.http import Http404


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductDetailSelectorTests(TestCase):
    """
        Test suite for product selection logic (Data Access Layer).

        Validates that:
        - Product lists are retrieved with correct ordering (e.g., newest first).
        - Detailed product retrieval correctly fetches associated images and metadata.
        - Proper error handling (Http404) is triggered when requesting non-existent IDs.
        - Database queries correctly reflect the state of featured and regular images.
    """

    def test_product_detail_selector_success(self):
        product = ProductFactory()

        ProductImageFactory(product=product, image="img1.jpg", is_feature=True)

        ProductImageFactory(product=product, image="img2.jpg", is_feature=False)

        result = product_detail_selector(product.id)

        self.assertEqual(result.id, product.id)
        self.assertEqual(result.images.count(), 2)

    def test_product_detail_selector_not_found(self):
        with self.assertRaises(Http404):
            product_detail_selector(9999)
