from django.test import TestCase, override_settings
from apps.product.serializers.product_detail_serializer import ProductDetailSerializer
from ..factories import ProductFactory, ProductImageFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductDetailSerializerTest(TestCase):
    """
        Test suite for the Product Detail view serializer.

        Validates the complex data mapping including:
        - Flattened relational fields (Brand name, Category title).
        - Nested serialization of multiple ProductImage objects.
        - Edge cases like products with no associated images to ensure consistent API responses.
    """

    def setUp(self):
        self.user = UserFactory(username="admin_user")
        self.product = ProductFactory(
            name="Gaming Laptop",
            user=self.user
        )
        self.img1 = ProductImageFactory(product=self.product, is_feature=True)
        self.img2 = ProductImageFactory(product=self.product, is_feature=False)

    def test_product_detail_serialization(self):
        serializer = ProductDetailSerializer(self.product)
        data = serializer.data

        self.assertEqual(data['name'], "Gaming Laptop")
        self.assertEqual(data['user'], "admin_user")
        self.assertEqual(data['brand_name'], self.product.brand.name)
        self.assertEqual(data['category'], self.product.category.title)

        self.assertEqual(len(data['images']), 2)

        image_data = data['images'][0]
        self.assertIn('id', image_data)
        self.assertIn('image', image_data)
        self.assertIn('is_feature', image_data)

    def test_product_detail_no_images(self):
        product_no_img = ProductFactory()
        serializer = ProductDetailSerializer(product_no_img)

        self.assertEqual(data := serializer.data['images'], [])
        self.assertEqual(len(data), 0)
