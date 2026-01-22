from django.test import TestCase, override_settings
from unittest.mock import patch
from rest_framework.exceptions import ValidationError
from apps.post.services.post_create_service import post_create_service
from apps.post.tests.factories import UserFactory, ProductFactory
from apps.post.models.post_model import Post


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostCreateServiceTest(TestCase):
    """
    Comprehensive test suite for the post_create_service.

    Verifies:
    - Data integrity through database persistence.
    - Proper error handling and logging for invalid data.
    - Transactional safety (rollback) during system failures.
    """

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()
        self.valid_data = {
            'product': self.product.id,
            'caption': 'Highly secure test caption',
            'price': 150.50,
            'location': 'Tehran',
            'is_active': True
        }

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_create_post_successfully(self, mock_logger):
        post = post_create_service(user=self.user, data=self.valid_data)

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.caption, 'Highly secure test caption')

        mock_logger.assert_called_once()
        self.assertIn(f"id={post.id}", mock_logger.call_args[0][0])

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_create_post_fails_on_invalid_price(self, mock_logger):
        invalid_data = self.valid_data.copy()
        invalid_data['price'] = -10.00

        with self.assertRaises(ValidationError):
            post_create_service(user=self.user, data=invalid_data)

        self.assertEqual(mock_logger.call_args[1]['status'], "ERROR")

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_atomic_rollback_on_unexpected_system_error(self, mock_logger):
        mock_logger.side_effect = Exception("Database Connection Lost during logging")

        with self.assertRaises(Exception):
            post_create_service(user=self.user, data=self.valid_data)

        self.assertEqual(Post.objects.count(), 0)

    @patch('apps.post.serializers.post_create_serializer.PostCreateSerializer.save')
    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_post_creation_critical_system_error(self, mock_log_activity, mock_save):
        """
        Tests the final 'except Exception' block (Line 34).
        Verifies that unexpected system crashes are logged as CRITICAL.
        """
        mock_save.side_effect = Exception("Unexpected Database Crash")

        with self.assertRaises(Exception):
            post_create_service(user=self.user, data=self.valid_data)

        mock_log_activity.assert_called_once()
        self.assertEqual(mock_log_activity.call_args[1].get('status'), "ERROR")
