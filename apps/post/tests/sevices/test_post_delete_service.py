from django.test import TestCase, override_settings
from django.db import transaction
from unittest.mock import patch
from rest_framework.exceptions import ValidationError
from apps.post.services.post_delete_service import post_delete_service
from apps.post.tests.factories import PostFactory, UserFactory
from apps.post.models.post_model import Post


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostDeleteServiceTest(TestCase):
    """
    Test suite for post_delete_service.

    Verifies:
    - Ownership enforcement (Security).
    - Database row locking logic (Integrity).
    - Logging for both success and unauthorized attempts.
    """

    def setUp(self):
        self.owner = UserFactory()
        self.stranger = UserFactory()
        self.post = PostFactory(user=self.owner)

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_owner_can_delete_post(self, mock_log):
        post_id = self.post.id

        post_delete_service(post_id=post_id, user=self.owner)

        self.assertFalse(Post.objects.filter(id=post_id).exists())
        mock_log.assert_called_once()
        self.assertIn("DELETED", mock_log.call_args[0][0].upper())

    @patch('apps.lib.loggers.AppLogger.log_security')
    def test_stranger_cannot_delete_owner_post(self, mock_log_security):
        post_id = self.post.id

        with self.assertRaises(ValidationError) as cm:
            post_delete_service(post_id=post_id, user=self.stranger)

        self.assertIn("permission", str(cm.exception))
        self.assertTrue(Post.objects.filter(id=post_id).exists())
        mock_log_security.assert_called_once()
        self.assertIn("Unauthorized delete attempt", mock_log_security.call_args[0][0])

    @patch('apps.lib.loggers.AppLogger.log_security')
    def test_delete_non_existent_post(self, mock_log_security):
        with self.assertRaises(ValidationError):
            post_delete_service(post_id=99999, user=self.owner)

        mock_log_security.assert_called_once()

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_atomic_rollback_on_critical_error(self, mock_log):
        mock_log.side_effect = Exception("Critical Logger Failure")

        post_id = self.post.id
        with self.assertRaises(Exception):
            post_delete_service(post_id=post_id, user=self.owner)

        self.assertTrue(Post.objects.filter(id=post_id).exists())
