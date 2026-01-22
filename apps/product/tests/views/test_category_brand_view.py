from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..factories import CategoryFactory, BrandFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CategoryListAPIViewTest(APITestCase):
    """
    Integration tests for the Category List API.

    Verifies that the endpoint is publicly accessible, returns the correct
    HTTP 200 status, and provides an ordered list of all categories
    matching the serializer structure.
    """

    def setUp(self):
        self.c1 = CategoryFactory(title="Z", slug="z")
        self.c2 = CategoryFactory(title="A", slug="a")
        self.url = reverse('product:category-list')

    def test_get_categories_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], self.c1.id)
        self.assertEqual(response.data[1]['id'], self.c2.id)


class BrandListAPIViewTest(APITestCase):
    """
    Integration tests for the Brand List API.

    Ensures the public brand endpoint operates correctly, confirming
    that brand data is serialized properly and the response
    matches the expected schema and ordering.
    """

    def setUp(self):
        self.b1 = BrandFactory()
        self.b2 = BrandFactory()
        self.url = reverse('product:brand-list')

    def test_get_brands_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.b1.name)
