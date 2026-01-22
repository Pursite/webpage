from django.test import TestCase, override_settings
from django.http import Http404
from apps.post.tests.factories import PostFactory, UserFactory
from apps.post.selectors.post_detail_selector import post_detail_selector


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostDetailSelectorTest(TestCase):
    """
        Test suite for the post_detail_selector.

        Verifies the access control logic for retrieving posts:
        - Active posts must be accessible by any user.
        - Inactive posts must only be accessible by their respective owners.
        - Accessing non-existent posts or inactive posts by non-owners must raise an Http404.
    """

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()

    def test_selector_returns_active_post_for_anyone(self):
        post = PostFactory(is_active=True)

        result = post_detail_selector(post_id=post.id)

        self.assertEqual(result, post)

    def test_selector_allows_owner_to_see_inactive_post(self):
        inactive_post = PostFactory(is_active=False, user=self.user)

        result = post_detail_selector(post_id=inactive_post.id, user=self.user)

        self.assertEqual(result, inactive_post)

    def test_selector_raises_404_for_inactive_post_and_stranger(self):
        inactive_post = PostFactory(is_active=False, user=self.user)

        with self.assertRaises(Http404):
            post_detail_selector(post_id=inactive_post.id, user=self.other_user)

    def test_selector_raises_404_if_post_does_not_exist(self):
        with self.assertRaises(Http404):
            post_detail_selector(post_id=9999)
