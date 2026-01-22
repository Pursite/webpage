from django.test import TestCase, override_settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from unittest.mock import patch
from apps.product.models.product_model import Product
from apps.product.tests.factories import ProductFactory, UserFactory
from ...services.product_delete_service import product_delete_service


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductDeleteServiceTest(TestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.other_user = UserFactory()
        self.product = ProductFactory(user=self.owner, name="Test Product")

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_delete_success_by_owner(self, mock_log):
        result = product_delete_service(product_id=self.product.id, user=self.owner)

        self.assertTrue(result)
        self.assertEqual(Product.objects.count(), 0)
        mock_log.assert_called()

    def test_delete_fail_unauthorized_user(self):
        with self.assertRaises(PermissionDenied):
            product_delete_service(product_id=self.product.id, user=self.other_user)

        self.assertEqual(Product.objects.count(), 1)

    def test_delete_non_existent_product(self):
        with self.assertRaises(Http404):
            product_delete_service(product_id=9999, user=self.owner)

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_delete_success_by_admin(self, mock_log):
        admin_user = UserFactory(is_staff=True)
        result = product_delete_service(product_id=self.product.id, user=admin_user)

        self.assertTrue(result)
        self.assertEqual(Product.objects.count(), 0)
