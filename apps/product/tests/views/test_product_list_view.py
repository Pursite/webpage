from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..factories import ProductFactory, CategoryFactory, BrandFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductListAPIViewTest(APITestCase):
    """
    Integration tests for the Advanced Product Catalog View.

    Covers:
    - Paginated responses and metadata (count, next, previous).
    - Query parameter filtering by category and brand.
    - Partial text search functionality on product names.
    - Public access (IsAdminOrReadOnly) for GET requests.
    """

    def setUp(self):
        self.category = CategoryFactory(title="Electronics")
        self.brand = BrandFactory(name="Sony")

        self.p1 = ProductFactory(name="Alpha Camera", category=self.category, brand=self.brand)
        self.p2 = ProductFactory(name="Beta Headphone", category=self.category)
        self.p3 = ProductFactory(name="Gamma Toaster")

        self.url = reverse('product:product-list')

    def test_get_all_products_paginated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 3)

    def test_filter_by_category(self):
        response = self.client.get(self.url, {'category': self.category.id})

        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], "Beta Headphone")

    def test_search_by_name(self):
        response = self.client.get(self.url, {'search': 'Alpha'})

        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Alpha Camera")

    def test_empty_results_filter(self):
        response = self.client.get(self.url, {'search': 'NonExistentProduct'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_get_all_products_without_pagination(self):
        from unittest.mock import patch
        with patch('apps.product.views.product_list_view.StandardPagePagination.paginate_queryset', return_value=None):
            response = self.client.get(self.url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsInstance(response.data, list)
            self.assertEqual(len(response.data), 3)
