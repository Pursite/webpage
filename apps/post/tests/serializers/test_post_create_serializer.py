from django.test import TestCase, override_settings
from apps.post.serializers.post_create_serializer import PostCreateSerializer
from apps.post.tests.factories import ProductFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostCreateSerializerTest(TestCase):
    """
    Test suite for PostCreateSerializer.

    Verifies:
    - Successful validation with correct data.
    - Field-level validation for 'price' (must be positive).
    - Read-only behavior of the 'user' field.
    - Requirement of mandatory fields like 'product'.
    """

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()

        self.valid_data = {
            'product': self.product.id,
            'caption': 'Test Caption',
            'price': 1500.00,
            'location': 'Tehran',
            'is_active': True
        }

    def test_serializer_with_valid_data(self):
        serializer = PostCreateSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['price'], 1500.00)

    def test_serializer_price_validation_fails(self):
        invalid_data = self.valid_data.copy()
        invalid_data['price'] = 0

        serializer = PostCreateSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
        self.assertEqual(serializer.errors['price'][0], "Price must be greater than 0")

    def test_serializer_negative_price_fails(self):
        invalid_data = self.valid_data.copy()
        invalid_data['price'] = -50.5

        serializer = PostCreateSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_user_field_is_read_only(self):
        data_with_user = self.valid_data.copy()
        data_with_user['user'] = 'hacker_user'  # سعی در تزریق کاربر

        serializer = PostCreateSerializer(data=data_with_user)
        self.assertTrue(serializer.is_valid())

        self.assertNotIn('user', serializer.validated_data)

    def test_required_fields(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['product']

        serializer = PostCreateSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('product', serializer.errors)
