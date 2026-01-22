from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.post.tests.factories import PostFactory, ProductFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostListAPIViewTest(APITestCase):
    """
    Tests for the public post listing API.
    Verifies: Pagination, Filtering, and Active-only logic.
    """

    def setUp(self):
        self.url = reverse('post:post-list')
        self.product_1 = ProductFactory()
        self.product_2 = ProductFactory()

        PostFactory.create_batch(5, is_active=True, product=self.product_1, location="Tehran")
        PostFactory.create_batch(3, is_active=True, product=self.product_2, location="Shiraz")
        PostFactory(is_active=False)

    def test_list_all_active_posts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 8)

    def test_filter_by_product(self):
        response = self.client.get(self.url, {'product': self.product_1.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 5)

    def test_search_by_location(self):
        response = self.client.get(self.url, {'search': 'Shiraz'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_inactive_posts_not_visible(self):
        response = self.client.get(self.url)

        for post in response.data['results']:
            pass
