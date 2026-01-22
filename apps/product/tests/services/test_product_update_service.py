from django.test import TestCase, override_settings
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from unittest.mock import patch

from apps.product.tests.factories import ProductFactory, UserFactory
from ...services.product_update_service import product_update_service


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductUpdateServiceTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.product = ProductFactory(user=self.user, name="Old Name")
        self.update_data = {'name': 'New Awesome Name'}

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_update_success_by_owner(self, mock_log):
        updated_product = product_update_service(
            product_id=self.product.id,
            user=self.user,
            data=self.update_data,
            partial=True
        )

        self.assertEqual(updated_product.name, 'New Awesome Name')
        mock_log.assert_called()

    def test_update_fail_unauthorized_user(self):
        with self.assertRaises(PermissionDenied):
            product_update_service(
                product_id=self.product.id,
                user=self.other_user,
                data=self.update_data
            )

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_update_validation_error_logging(self, mock_log):
        invalid_data = {'name': ''}

        with self.assertRaises(ValidationError):
            product_update_service(
                product_id=self.product.id,
                user=self.user,
                data=invalid_data,
                partial=True
            )

        self.assertEqual(mock_log.call_args[1]['status'], "ERROR")

    def test_partial_update_verification(self):
        old_brand = self.product.brand
        product_update_service(
            product_id=self.product.id,
            user=self.user,
            data={'name': 'Changed Only Name'},
            partial=True
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.brand, old_brand)
