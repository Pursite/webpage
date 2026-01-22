from django.test import TestCase, override_settings
from rest_framework.exceptions import ValidationError
from unittest.mock import patch
from apps.product.models.product_model import Product
from ..factories import UserFactory, CategoryFactory, BrandFactory
from ...services.product_create_service import product_create_service


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductCreateServiceTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.brand = BrandFactory()
        self.valid_data = {
            'name': 'Pro Tablet',
            'category': self.category.id,
            'brand': self.brand.id
        }

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_product_create_success(self, mock_log):
        product = product_create_service(user=self.user, data=self.valid_data)

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.user, self.user)
        mock_log.assert_called()
        self.assertIn("Product Created", mock_log.call_args_list[0][0][0])

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_product_create_validation_error(self, mock_log):
        invalid_data = {'name': ''}

        with self.assertRaises(ValidationError):
            product_create_service(user=self.user, data=invalid_data)

        self.assertEqual(mock_log.call_args[1]['status'], "ERROR")

    def test_atomic_rollback_on_error(self):
        with patch('apps.lib.loggers.AppLogger.log_activity') as mock_log:
            mock_log.side_effect = Exception("System Crash")

            with self.assertRaises(Exception):
                product_create_service(user=self.user, data=self.valid_data)

            self.assertEqual(Product.objects.count(), 0)
