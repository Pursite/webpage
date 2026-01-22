from django.test import TestCase, override_settings
from apps.product.serializers.product_create_serializer import ProductCreateSerializer
from ..factories import CategoryFactory, BrandFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductCreateSerializerTest(TestCase):
    """
        Test suite for Product creation via Serializer.

        Focuses on:
        - Data integrity: Ensuring valid IDs for Brand and Category are correctly mapped to model instances.
        - Security: Verifying that 'read_only_fields' (like 'user') cannot be manipulated by external payloads.
        - Validation: Confirming that missing mandatory fields trigger appropriate error responses.
    """

    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.brand = BrandFactory()

        self.valid_payload = {
            'name': 'New Gaming Mouse',
            'category': self.category.id,
            'brand': self.brand.id
        }

    def test_product_create_valid_data(self):
        serializer = ProductCreateSerializer(data=self.valid_payload)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'New Gaming Mouse')
        self.assertEqual(serializer.validated_data['category'], self.category)
        self.assertEqual(serializer.validated_data['brand'], self.brand)

    def test_product_create_user_is_readonly(self):
        another_user = UserFactory()
        payload = self.valid_payload.copy()
        payload['user'] = another_user.id  # سعی در تزریق یوزر غیرمجاز

        serializer = ProductCreateSerializer(data=payload)
        self.assertTrue(serializer.is_valid())

        self.assertNotIn('user', serializer.validated_data)

    def test_product_create_missing_fields(self):
        serializer = ProductCreateSerializer(data={'name': 'Incomplete Product'})

        self.assertFalse(serializer.is_valid())
        self.assertIn('category', serializer.errors)
        self.assertIn('brand', serializer.errors)
