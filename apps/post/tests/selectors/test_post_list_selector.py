from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from apps.post.tests.factories import PostFactory
from apps.post.selectors.post_list_selector import post_list_selector


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostListSelectorTest(TestCase):
    """
    Test suite for the post_list_selector.

    Verifies that:
    - Only active posts are returned by default.
    - Posts are correctly ordered by their creation date (descending).
    - Integrated filter backends are correctly applied to the queryset.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.active_post1 = PostFactory(is_active=True)
        self.active_post2 = PostFactory(is_active=True)
        self.inactive_post = PostFactory(is_active=False)

        class MockView(APIView):
            filter_backends = []

        self.view = MockView()

    def test_selector_returns_only_active_posts(self):
        request = self.factory.get('/')

        queryset = post_list_selector(request=request, view=self.view)

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.active_post1, queryset)
        self.assertIn(self.active_post2, queryset)
        self.assertNotIn(self.inactive_post, queryset)

    def test_selector_ordering_by_created_at_descending(self):
        request = self.factory.get('/')

        queryset = post_list_selector(request=request, view=self.view)

        self.assertEqual(queryset[0], self.active_post2)
        self.assertEqual(queryset[1], self.active_post1)

    def test_selector_applies_filter_backends(self):
        from rest_framework.request import Request
        self.view.filter_backends = [SearchFilter]
        self.view.search_fields = ['caption']

        self.active_post1.caption = "Target Content"
        self.active_post1.save()

        raw_request = self.factory.get('/', {'search': 'Target Content'})

        drf_request = self.view.initialize_request(raw_request)

        queryset = post_list_selector(request=drf_request, view=self.view)

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0], self.active_post1)
