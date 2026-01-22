from django.test import TestCase, override_settings
from unittest.mock import patch
from rest_framework.exceptions import ValidationError
from apps.post.services.post_update_service import post_update_service
from apps.post.tests.factories import PostFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostUpdateServiceTest(TestCase):
    """
    Test suite for post_update_service.

    Verifies:
    - Full update (PUT) vs Partial update (PATCH) logic.
    - Security: Only the post owner can perform updates.
    - Data Integrity: Database locking and logging accuracy.
    """

    def setUp(self):
        self.owner = UserFactory()
        self.stranger = UserFactory()
        self.post = PostFactory(user=self.owner, caption="Old Caption", price=100.00)

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_full_update_by_owner_success(self, mock_log):
        update_data = {
            'product': self.post.product.id,
            'caption': "New Brand New Caption",
            'price': 200.00,
            'location': 'New York',
            'is_active': True
        }

        updated_post = post_update_service(
            post_id=self.post.id, user=self.owner, data=update_data, partial=False
        )

        self.assertEqual(updated_post.caption, "New Brand New Caption")
        self.assertEqual(float(updated_post.price), 200.00)
        self.assertIn("(PUT)", mock_log.call_args[0][0])

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_partial_update_by_owner_success(self, mock_log):
        update_data = {'caption': "Only Caption Changed"}

        updated_post = post_update_service(
            post_id=self.post.id, user=self.owner, data=update_data, partial=True
        )

        self.assertEqual(updated_post.caption, "Only Caption Changed")
        self.assertEqual(float(updated_post.price), 100.00)
        self.assertIn("(PATCH)", mock_log.call_args[0][0])

    @patch('apps.lib.loggers.AppLogger.log_security')
    def test_update_by_stranger_fails(self, mock_log_security):
        update_data = {'caption': "Hacked!"}

        with self.assertRaises(ValidationError) as cm:
            post_update_service(post_id=self.post.id, user=self.stranger, data=update_data, partial=True)

        self.assertIn("permission to edit", str(cm.exception))
        mock_log_security.assert_called_once()
        self.post.refresh_from_db()
        self.assertEqual(self.post.caption, "Old Caption")

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_update_fails_on_invalid_data(self, mock_log):
        update_data = {'price': -50.00}

        with self.assertRaises(ValidationError):
            post_update_service(post_id=self.post.id, user=self.owner, data=update_data, partial=True)

        self.assertEqual(mock_log.call_args[1]['status'], "ERROR")

    def test_update_post_not_found(self):
        with self.assertRaises(ValidationError) as cm:
            post_update_service(post_id=99999, user=self.owner, data={})
        self.assertIn("Post not found", str(cm.exception))

    @patch('apps.post.serializers.post_create_serializer.PostCreateSerializer.save')
    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_update_service_critical_system_error(self, mock_log, mock_save):
        mock_save.side_effect = Exception("Unexpected System Crash")

        with self.assertRaises(Exception):
            post_update_service(post_id=self.post.id, user=self.owner, data={'caption': 'test'}, partial=True)

        # بررسی ثبت لاگ CRITICAL
        self.assertEqual(mock_log.call_args[1]['status'], "CRITICAL")
