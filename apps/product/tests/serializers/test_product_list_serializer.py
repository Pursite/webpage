from django.test import TestCase, RequestFactory, override_settings
from apps.product.serializers.product_list_serializer import ProductListSerializer
from apps.product.models.product_image_model import ProductImage
from ..factories import ProductFactory, UserFactory, ProductImageFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductListSerializerTest(TestCase):
    """
        Test suite for the optimized Product List serializer.

        Specifically tests the 'thumbnail' SerializerMethodField logic:
        - Priority 1: Returns the 'is_feature' image.
        - Priority 2: Falls back to the first available image if no feature image exists.
        - Priority 3: Returns None if the image gallery is empty.
        - Context handling: Verifies absolute URI generation when a request object is present.
    """

    def setUp(self):
        self.user = UserFactory(username="parsa_dev")
        self.product = ProductFactory(name="Laptop Pro", user=self.user)
        self.factory = RequestFactory()

    def test_product_list_serialization_basic_fields(self):
        serializer = ProductListSerializer(self.product)
        data = serializer.data

        self.assertEqual(data['name'], "Laptop Pro")
        self.assertEqual(data['user'], "parsa_dev")
        self.assertEqual(data['brand_name'], self.product.brand.name)
        self.assertEqual(data['category_title'], self.product.category.title)

    def test_thumbnail_with_is_feature_image(self):
        ProductImageFactory(product=self.product, image="normal.jpg", is_feature=False)
        feature_img = ProductImage.objects.create(product=self.product, image="feature.jpg", is_feature=True)

        serializer = ProductListSerializer(self.product)
        self.assertIn("feature.jpg", serializer.data['thumbnail'])

    def test_thumbnail_fallback_to_first_image(self):
        ProductImageFactory(product=self.product, image="first.jpg", is_feature=False)

        serializer = ProductListSerializer(self.product)
        self.assertIn("first.jpg", serializer.data['thumbnail'])

    def test_thumbnail_none_if_no_images(self):
        serializer = ProductListSerializer(self.product)
        self.assertIsNone(serializer.data['thumbnail'])

    def test_thumbnail_with_request_context(self):
        ProductImageFactory(product=self.product, image="test.jpg")
        request = self.factory.get('/')

        serializer = ProductListSerializer(self.product, context={'request': request})

        self.assertTrue(serializer.data['thumbnail'].startswith('http://testserver/'))
